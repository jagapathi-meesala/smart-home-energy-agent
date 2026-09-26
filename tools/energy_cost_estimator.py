from typing import Any, Dict, List, Optional, Tuple
from contracts.input_contract import InputContract
from tools.tool_registry import BaseTool

class EnergyCostEstimatorTool(BaseTool):
    name = "energy_cost_estimator_tool"
    description = "Estimate electricity cost based on total consumption kWh and dynamic tariff rate."
    capability = "energy_cost_estimation"

    def execute(self, records: List[Dict[str, Any]], tariff_per_kwh: Optional[float] = None, **kwargs) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]]]:
        if not records:
            return False, {}, {
                "code": "EMPTY_DATASET",
                "message": "Cannot estimate costs for an empty dataset."
            }

        # Resolve tariff from kwargs or records
        resolved_tariff = tariff_per_kwh
        if resolved_tariff is None:
            # Check if any record has tariff_per_kwh
            for r in records:
                if "tariff_per_kwh" in r and r["tariff_per_kwh"] is not None:
                    resolved_tariff = r["tariff_per_kwh"]
                    break

        is_valid_t, tariff_val, err = InputContract.validate_tariff(resolved_tariff)
        if not is_valid_t or tariff_val is None:
            return False, {}, err or {
                "code": "INVALID_TARIFF",
                "message": "Electricity tariff rate is missing or invalid. Please supply tariff_per_kwh."
            }

        total_kwh = sum(r["energy_kwh"] for r in records)
        estimated_cost = total_kwh * tariff_val

        result = {
            "total_consumption_kwh": round(total_kwh, 4),
            "tariff_per_kwh": round(tariff_val, 4),
            "estimated_cost": round(estimated_cost, 4),
            "currency": "USD",
            "calculation_explanation": f"estimated_cost ({round(estimated_cost, 4)}) = energy_kwh ({round(total_kwh, 4)}) × tariff_per_kwh ({round(tariff_val, 4)})"
        }

        return True, result, None
