import math
import statistics
from typing import Any, Dict, List, Optional, Tuple
from tools.tool_registry import BaseTool

class EnergyAnomalyDetectorTool(BaseTool):
    name = "energy-anomaly-detector"
    description = "Identify unusual energy consumption records using deterministic statistical methods (Z-score, IQR, threshold)."
    capability = "energy_anomaly_detection"

    def execute(
        self,
        records: List[Dict[str, Any]],
        method: str = "z_score",
        z_threshold: float = 2.0,
        iqr_multiplier: float = 1.5,
        abs_threshold: Optional[float] = None,
        **kwargs
    ) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:

        if not records:
            return False, {}, {
                "code": "EMPTY_DATASET",
                "message": "Cannot perform anomaly detection on an empty dataset."
            }

        kwh_values = [r["energy_kwh"] for r in records]
        count = len(kwh_values)
        mean_val = statistics.mean(kwh_values) if count > 0 else 0.0
        std_val = statistics.stdev(kwh_values) if count > 1 else 0.0

        anomalies: List[Dict[str, Any]] = []

        if method == "iqr":
            sorted_vals = sorted(kwh_values)
            q1 = statistics.median(sorted_vals[:count // 2]) if count >= 2 else sorted_vals[0]
            q3 = statistics.median(sorted_vals[(count + 1) // 2:]) if count >= 2 else sorted_vals[-1]
            iqr = q3 - q1
            upper_bound = q3 + (iqr_multiplier * iqr)
            lower_bound = q1 - (iqr_multiplier * iqr)

            for rec in records:
                val = rec["energy_kwh"]
                if val > upper_bound or val < lower_bound:
                    diff = abs(val - mean_val)
                    score = diff / (iqr if iqr > 0 else 1.0)
                    anomalies.append({
                        "record": rec,
                        "anomaly_score": round(score, 4),
                        "value_kwh": val,
                        "explanation": f"Record value ({val} kWh) falls outside IQR bounds [{round(lower_bound, 4)}, {round(upper_bound, 4)}]."
                    })
            config_desc = {"method": "IQR", "iqr_multiplier": iqr_multiplier, "q1": round(q1, 4), "q3": round(q3, 4), "iqr": round(iqr, 4)}

        elif method == "threshold" and abs_threshold is not None:
            for rec in records:
                val = rec["energy_kwh"]
                if val >= abs_threshold:
                    anomalies.append({
                        "record": rec,
                        "anomaly_score": round(val / abs_threshold, 4),
                        "value_kwh": val,
                        "explanation": f"Record consumption ({val} kWh) exceeds configurable absolute threshold ({abs_threshold} kWh)."
                    })
            config_desc = {"method": "threshold", "threshold_kwh": abs_threshold}

        else:
            # Default Z-score method
            method = "z_score"
            for rec in records:
                val = rec["energy_kwh"]
                z_score = ((val - mean_val) / std_val) if std_val > 0 else 0.0
                if abs(z_score) >= z_threshold:
                    anomalies.append({
                        "record": rec,
                        "anomaly_score": round(abs(z_score), 4),
                        "value_kwh": val,
                        "explanation": f"Record consumption ({val} kWh) has Z-score of {round(z_score, 4)}, exceeding standard threshold of {z_threshold}."
                    })
            config_desc = {"method": "Z-score", "z_threshold": z_threshold, "mean_kwh": round(mean_val, 4), "std_dev_kwh": round(std_val, 4)}

        result = {
            "detection_method": method,
            "configuration": config_desc,
            "total_records_analyzed": count,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies
        }

        return True, result, None
