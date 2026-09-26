import json
import csv
import io
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union, Optional

class InputContract:
    """Validates raw energy consumption datasets (JSON/CSV) and parameters."""

    @staticmethod
    def parse_input_records(raw_input: Union[str, List[Dict[str, Any]]]) -> Tuple[bool, List[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Parses raw input (JSON string, CSV string, or Python list) into structured records.
        Returns: (is_valid, records, error_dict)
        """
        if raw_input is None:
            return False, [], {
                "code": "INVALID_INPUT",
                "message": "Input data is None."
            }

        records: List[Dict[str, Any]] = []

        if isinstance(raw_input, list):
            records = raw_input
        elif isinstance(raw_input, str):
            trimmed = raw_input.strip()
            if not trimmed:
                return False, [], {
                    "code": "EMPTY_DATASET",
                    "message": "Input string dataset is empty."
                }
            
            # Try JSON first
            if trimmed.startswith("[") or trimmed.startswith("{"):
                try:
                    parsed = json.loads(trimmed)
                    if isinstance(parsed, list):
                        records = parsed
                    elif isinstance(parsed, dict):
                        if "records" in parsed and isinstance(parsed["records"], list):
                            records = parsed["records"]
                        else:
                            records = [parsed]
                    else:
                        return False, [], {
                            "code": "MALFORMED_DATA",
                            "message": "Parsed JSON is not a list or dictionary record."
                        }
                except json.JSONDecodeError as e:
                    return False, [], {
                        "code": "INVALID_INPUT",
                        "message": f"Invalid JSON input payload: {str(e)}"
                    }
            else:
                # Try CSV parsing
                try:
                    reader = csv.DictReader(io.StringIO(trimmed))
                    records = [row for row in reader]
                    if not records:
                        return False, [], {
                            "code": "EMPTY_DATASET",
                            "message": "CSV dataset contains no data rows."
                        }
                except Exception as e:
                    return False, [], {
                        "code": "MALFORMED_DATA",
                        "message": f"Malformed CSV input payload: {str(e)}"
                    }
        else:
            return False, [], {
                "code": "INVALID_INPUT",
                "message": f"Unsupported input type: {type(raw_input).__name__}"
            }

        if not records:
            return False, [], {
                "code": "EMPTY_DATASET",
                "message": "Energy dataset is empty."
            }

        return True, records, None

    @classmethod
    def validate_records(cls, records: List[Dict[str, Any]], require_device: bool = False) -> Tuple[bool, List[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Validates parsed records for required fields, numeric energy values, and timestamp formats.
        Returns cleaned/validated records or error details.
        """
        if not records:
            return False, [], {
                "code": "EMPTY_DATASET",
                "message": "Dataset contains no records to validate."
            }

        validated: List[Dict[str, Any]] = []

        for idx, rec in enumerate(records):
            if not isinstance(rec, dict):
                return False, [], {
                    "code": "MALFORMED_DATA",
                    "message": f"Record at index {idx} is not a valid JSON object/dictionary."
                }

            # Check timestamp
            ts_val = rec.get("timestamp")
            if ts_val is None or str(ts_val).strip() == "":
                return False, [], {
                    "code": "MISSING_FIELD",
                    "message": f"Record at index {idx} is missing required 'timestamp' field."
                }
            
            # Check numeric energy_kwh
            if "energy_kwh" not in rec or rec.get("energy_kwh") is None:
                return False, [], {
                    "code": "MISSING_FIELD",
                    "message": f"Record at index {idx} is missing required 'energy_kwh' field."
                }

            try:
                energy_val = float(rec["energy_kwh"])
            except (ValueError, TypeError):
                return False, [], {
                    "code": "INVALID_ENERGY_VALUE",
                    "message": f"Record at index {idx} has non-numeric energy_kwh value: '{rec.get('energy_kwh')}'."
                }

            if energy_val < 0:
                return False, [], {
                    "code": "INVALID_ENERGY_VALUE",
                    "message": f"Record at index {idx} has negative energy consumption: {energy_val} kWh."
                }

            # Device / Appliance field normalization
            device = rec.get("device") or rec.get("appliance") or rec.get("category") or "unknown_device"
            if require_device and (device == "unknown_device" or not str(device).strip()):
                return False, [], {
                    "code": "MISSING_FIELD",
                    "message": f"Record at index {idx} requires an appliance/device category field."
                }

            # Duration
            duration = rec.get("duration_minutes") or rec.get("duration") or 60
            try:
                duration_val = float(duration)
            except (ValueError, TypeError):
                duration_val = 60.0

            clean_rec = {
                "timestamp": str(ts_val),
                "device": str(device),
                "energy_kwh": energy_val,
                "duration_minutes": duration_val
            }

            if "tariff_per_kwh" in rec and rec["tariff_per_kwh"] is not None:
                try:
                    clean_rec["tariff_per_kwh"] = float(rec["tariff_per_kwh"])
                except (ValueError, TypeError):
                    pass

            validated.append(clean_rec)

        return True, validated, None

    @staticmethod
    def validate_tariff(tariff: Optional[Any]) -> Tuple[bool, Optional[float], Optional[Dict[str, Any]]]:
        """Validates electricity tariff parameter."""
        if tariff is None:
            return False, None, {
                "code": "INVALID_TARIFF",
                "message": "Tariff parameter is missing."
            }
        try:
            t_val = float(tariff)
            if t_val < 0:
                return False, None, {
                    "code": "INVALID_TARIFF",
                    "message": f"Tariff cannot be negative: {t_val}"
                }
            return True, t_val, None
        except (ValueError, TypeError):
            return False, None, {
                "code": "INVALID_TARIFF",
                "message": f"Tariff value must be a valid numeric float: '{tariff}'."
            }
