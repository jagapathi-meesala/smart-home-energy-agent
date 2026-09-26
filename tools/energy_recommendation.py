from typing import Any, Dict, List, Optional, Tuple
from tools.appliance_energy_analyzer import ApplianceEnergyAnalyzerTool
from tools.energy_anomaly_detector import EnergyAnomalyDetectorTool
from tools.energy_pattern_detector import EnergyPatternDetectorTool
from tools.tool_registry import BaseTool

class EnergyRecommendationTool(BaseTool):
    name = "energy_recommendation_tool"
    description = "Generate analytical energy-saving recommendations based on statistical usage metrics."
    capability = "energy_saving_recommendation"

    def execute(self, records: List[Dict[str, Any]], **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        if not records:
            return False, {}, {
                "code": "EMPTY_DATASET",
                "message": "Cannot generate recommendations for an empty dataset."
            }

        recommendations: List[Dict[str, Any]] = []

        # 1. Appliance breakdown analysis for high consumption
        appliance_tool = ApplianceEnergyAnalyzerTool()
        ok_app, app_res, _ = appliance_tool.execute(records)
        if ok_app and "highest_consumption_categories" in app_res:
            categories = app_res["highest_consumption_categories"]
            if categories:
                top_cat = categories[0]
                if top_cat["percentage"] > 30.0:
                    recommendations.append({
                        "category": "High Consumption Appliance Review",
                        "target_device": top_cat["category"],
                        "recommendation": f"Device category '{top_cat['category']}' accounts for {top_cat['percentage']}% of total energy consumption. Review operational schedule, temperature settings, or efficiency rating.",
                        "analytical_basis": f"Consumes {top_cat['total_kwh']} kWh out of total dataset consumption."
                    })

        # 2. Peak pattern analysis
        pattern_tool = EnergyPatternDetectorTool()
        ok_pat, pat_res, _ = pattern_tool.execute(records)
        if ok_pat and pat_res.get("peak_usage_period") != "N/A":
            peak_period = pat_res["peak_usage_period"]
            recommendations.append({
                "category": "Load Shifting Opportunity",
                "target_period": peak_period,
                "recommendation": f"Peak energy consumption is concentrated around {peak_period}. Consider shifting flexible, non-critical appliance loads (e.g., dishwasher, laundry) away from peak hours.",
                "analytical_basis": f"Identified peak hourly consumption period at {peak_period}."
            })

        # 3. Anomaly analysis
        anomaly_tool = EnergyAnomalyDetectorTool()
        ok_anom, anom_res, _ = anomaly_tool.execute(records)
        if ok_anom and anom_res.get("anomaly_count", 0) > 0:
            anom_count = anom_res["anomaly_count"]
            recommendations.append({
                "category": "Anomaly & Defect Inspection",
                "target_count": anom_count,
                "recommendation": f"Detected {anom_count} unusual energy consumption spike(s). Inspect highlighted device records for potential equipment malfunction or unintended continuous running.",
                "analytical_basis": f"{anom_count} records exceeded standard statistical variance thresholds."
            })

        if not recommendations:
            recommendations.append({
                "category": "General Maintenance",
                "recommendation": "Energy consumption across all categories and time windows is evenly distributed within normal parameters. Maintain regular appliance servicing.",
                "analytical_basis": "No dominant appliance category (>30%) or significant statistical anomaly was detected."
            })

        result = {
            "total_recommendations": len(recommendations),
            "recommendations": recommendations,
            "disclaimer": "LIMITATION DISCLAIMER: These suggestions are analytical data summaries generated algorithmically from statistical metrics. They do NOT constitute certified electrical engineering advice, professional building audits, or safety inspections."
        }

        return True, result, None
