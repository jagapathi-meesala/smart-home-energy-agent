from typing import Any, Dict, List, Optional, Tuple
from tools.tool_registry import BaseTool

class ApplianceEnergyAnalyzerTool(BaseTool):
    name = "appliance-energy-analyzer"
    description = "Analyze energy consumption by appliance/device category dynamically."
    capability = "appliance_energy_analysis"

    def execute(self, records: List[Dict[str, Any]], **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        if not records:
            return False, {}, {
                "code": "EMPTY_DATASET",
                "message": "Cannot perform appliance energy analysis on empty dataset."
            }

        total_overall_kwh = sum(r["energy_kwh"] for r in records)
        category_data: Dict[str, Dict[str, Any]] = {}

        for rec in records:
            dev = str(rec.get("device", "unknown_device"))
            kwh = rec["energy_kwh"]
            duration = rec.get("duration_minutes", 60.0)

            if dev not in category_data:
                category_data[dev] = {
                    "total_kwh": 0.0,
                    "record_count": 0,
                    "total_duration_minutes": 0.0,
                    "peak_kwh": 0.0
                }

            category_data[dev]["total_kwh"] += kwh
            category_data[dev]["record_count"] += 1
            category_data[dev]["total_duration_minutes"] += duration
            if kwh > category_data[dev]["peak_kwh"]:
                category_data[dev]["peak_kwh"] = kwh

        appliance_breakdown = {}
        for dev, stats in category_data.items():
            dev_total = stats["total_kwh"]
            pct = (dev_total / total_overall_kwh * 100.0) if total_overall_kwh > 0 else 0.0
            appliance_breakdown[dev] = {
                "total_kwh": round(dev_total, 4),
                "percentage_contribution": round(pct, 2),
                "record_count": stats["record_count"],
                "average_kwh_per_record": round(dev_total / stats["record_count"], 4),
                "peak_kwh": round(stats["peak_kwh"], 4)
            }

        # Sort highest consumption categories
        sorted_categories = sorted(
            appliance_breakdown.items(),
            key=lambda x: x[1]["total_kwh"],
            reverse=True
        )

        highest_consumption_categories = [
            {"category": cat, "total_kwh": data["total_kwh"], "percentage": data["percentage_contribution"]}
            for cat, data in sorted_categories
        ]

        result = {
            "appliance_breakdown": appliance_breakdown,
            "highest_consumption_categories": highest_consumption_categories,
            "total_categories_analyzed": len(appliance_breakdown),
            "overall_total_kwh": round(total_overall_kwh, 4)
        }

        return True, result, None
