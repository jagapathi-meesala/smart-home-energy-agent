from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from tools.tool_registry import BaseTool

class EnergyPatternDetectorTool(BaseTool):
    name = "energy_pattern_detector_tool"
    description = "Detect temporal energy usage patterns deterministically (hourly, daily, weekday/weekend)."
    capability = "energy_pattern_detection"

    def execute(self, records: List[Dict[str, Any]], **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        if not records:
            return False, {}, {
                "code": "EMPTY_DATASET",
                "message": "Cannot detect patterns on an empty dataset."
            }

        hourly_totals: Dict[int, float] = {h: 0.0 for h in range(24)}
        hourly_counts: Dict[int, int] = {h: 0 for h in range(24)}

        weekday_kwh = 0.0
        weekday_count = 0
        weekend_kwh = 0.0
        weekend_count = 0

        daily_totals: Dict[str, float] = {}

        for rec in records:
            ts_str = rec.get("timestamp", "")
            kwh = rec.get("energy_kwh", 0.0)

            try:
                dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                # Fallback simple string parser or skip hour grouping
                dt = None

            if dt:
                hr = dt.hour
                hourly_totals[hr] += kwh
                hourly_counts[hr] += 1

                day_key = dt.strftime("%Y-%m-%d")
                daily_totals[day_key] = daily_totals.get(day_key, 0.0) + kwh

                if dt.weekday() < 5:  # Monday - Friday
                    weekday_kwh += kwh
                    weekday_count += 1
                else:  # Saturday - Sunday
                    weekend_kwh += kwh
                    weekend_count += 1

        hourly_patterns = {}
        for h in range(24):
            avg_h = (hourly_totals[h] / hourly_counts[h]) if hourly_counts[h] > 0 else 0.0
            hourly_patterns[f"{h:02d}:00"] = {
                "total_kwh": round(hourly_totals[h], 4),
                "record_count": hourly_counts[h],
                "average_kwh": round(avg_h, 4)
            }

        # Identify peak and low usage hours
        active_hours = [(h, (hourly_totals[h] / hourly_counts[h])) for h in range(24) if hourly_counts[h] > 0]
        if active_hours:
            peak_hour_tuple = max(active_hours, key=lambda x: x[1])
            low_hour_tuple = min(active_hours, key=lambda x: x[1])
            peak_usage_period = f"{peak_hour_tuple[0]:02d}:00"
            low_usage_period = f"{low_hour_tuple[0]:02d}:00"
        else:
            peak_usage_period = "N/A"
            low_usage_period = "N/A"

        avg_weekday = (weekday_kwh / weekday_count) if weekday_count > 0 else 0.0
        avg_weekend = (weekend_kwh / weekend_count) if weekend_count > 0 else 0.0

        result = {
            "hourly_patterns": hourly_patterns,
            "peak_usage_period": peak_usage_period,
            "low_usage_period": low_usage_period,
            "weekday_vs_weekend": {
                "weekday_total_kwh": round(weekday_kwh, 4),
                "weekday_average_kwh": round(avg_weekday, 4),
                "weekend_total_kwh": round(weekend_kwh, 4),
                "weekend_average_kwh": round(avg_weekend, 4),
                "comparison": "higher_weekend" if avg_weekend > avg_weekday else ("higher_weekday" if avg_weekday > avg_weekend else "equal")
            },
            "daily_totals": {k: round(v, 4) for k, v in daily_totals.items()}
        }

        return True, result, None
