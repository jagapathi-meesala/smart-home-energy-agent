from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from tools.appliance_energy_analyzer import ApplianceEnergyAnalyzerTool
from tools.energy_anomaly_detector import EnergyAnomalyDetectorTool
from tools.energy_consumption_analyzer import EnergyConsumptionAnalyzerTool
from tools.energy_cost_estimator import EnergyCostEstimatorTool
from tools.energy_pattern_detector import EnergyPatternDetectorTool
from tools.energy_recommendation import EnergyRecommendationTool
from tools.tool_registry import BaseTool

class EnergyReportTool(BaseTool):
    name = "energy_report_tool"
    description = "Generate a comprehensive structured JSON energy report synthesizing all analysis modules."
    capability = "energy_reporting"

    def execute(self, records: List[Dict[str, Any]], tariff_per_kwh: Optional[float] = None, **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        if not records:
            return False, {}, {
                "code": "EMPTY_DATASET",
                "message": "Cannot generate energy report for an empty dataset."
            }

        # 1. Consumption analysis
        _, consumption_res, _ = EnergyConsumptionAnalyzerTool().execute(records)

        # 2. Appliance breakdown
        _, appliance_res, _ = ApplianceEnergyAnalyzerTool().execute(records)

        # 3. Pattern detection
        _, pattern_res, _ = EnergyPatternDetectorTool().execute(records)

        # 4. Anomaly detection
        _, anomaly_res, _ = EnergyAnomalyDetectorTool().execute(records)

        # 5. Cost estimation
        ok_cost, cost_res, _ = EnergyCostEstimatorTool().execute(records, tariff_per_kwh=tariff_per_kwh)
        cost_data = cost_res if ok_cost else {"status": "skipped", "reason": "No valid tariff supplied"}

        # 6. Recommendations
        _, rec_res, _ = EnergyRecommendationTool().execute(records)

        report = {
            "summary": {
                "total_records": len(records),
                "total_energy_kwh": consumption_res.get("total_energy_kwh", 0.0),
                "average_energy_kwh": consumption_res.get("average_energy_kwh", 0.0),
                "peak_consumption_kwh": consumption_res.get("peak_consumption", {}).get("energy_kwh", 0.0),
                "anomalies_detected": anomaly_res.get("anomaly_count", 0),
                "estimated_cost": cost_data.get("estimated_cost", "N/A")
            },
            "consumption_analysis": consumption_res,
            "appliance_breakdown": appliance_res.get("appliance_breakdown", {}),
            "detected_patterns": pattern_res,
            "detected_anomalies": anomaly_res,
            "estimated_cost": cost_data,
            "recommendations": rec_res.get("recommendations", []),
            "limitations": [
                rec_res.get("disclaimer", "System provides analytical suggestions only.")
            ],
            "analysis_metadata": {
                "agent_id": "smart-home-energy-agent-01",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "execution_mode": "offline_deterministic"
            }
        }

        return True, report, None
