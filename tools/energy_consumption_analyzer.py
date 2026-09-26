import math
import statistics
from typing import Any, Dict, List, Optional, Tuple
from tools.tool_registry import BaseTool

class EnergyConsumptionAnalyzerTool(BaseTool):
    name = "energy_consumption_analyzer_tool"
    description = "Analyze generic energy-consumption records for peak, average, minimum, total, and distribution metrics."
    capability = "energy_consumption_analysis"

    def execute(self, records: List[Dict[str, Any]], **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        if not records:
            return False, {}, {
                "code": "EMPTY_DATASET",
                "message": "Cannot perform energy consumption analysis on empty dataset."
            }

        kwh_values = [r["energy_kwh"] for r in records]
        total_kwh = sum(kwh_values)
        count = len(kwh_values)
        avg_kwh = total_kwh / count if count > 0 else 0.0

        max_val = max(kwh_values)
        min_val = min(kwh_values)

        peak_record = next(r for r in records if r["energy_kwh"] == max_val)
        min_record = next(r for r in records if r["energy_kwh"] == min_val)

        sorted_vals = sorted(kwh_values)
        median_val = statistics.median(sorted_vals)
        std_dev = statistics.stdev(sorted_vals) if count > 1 else 0.0

        total_duration_minutes = sum(r.get("duration_minutes", 60.0) for r in records)

        result = {
            "total_energy_kwh": round(total_kwh, 4),
            "average_energy_kwh": round(avg_kwh, 4),
            "peak_consumption": {
                "energy_kwh": round(max_val, 4),
                "timestamp": peak_record.get("timestamp"),
                "device": peak_record.get("device")
            },
            "minimum_consumption": {
                "energy_kwh": round(min_val, 4),
                "timestamp": min_record.get("timestamp"),
                "device": min_record.get("device")
            },
            "consumption_distribution": {
                "median_kwh": round(median_val, 4),
                "std_dev_kwh": round(std_dev, 4),
                "record_count": count
            },
            "time_statistics": {
                "record_count": count,
                "total_duration_hours": round(total_duration_minutes / 60.0, 2)
            }
        }

        return True, result, None
