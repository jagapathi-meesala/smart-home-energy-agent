from contracts.input_contract import InputContract
from contracts.output_contract import OutputContract
from contracts.behavior_contract import BehaviorContract

def test_input_contract_json_parsing():
    raw_json = '[{"timestamp": "2026-09-01T10:00:00", "energy_kwh": 1.5}]'
    is_valid, records, err = InputContract.parse_input_records(raw_json)
    assert is_valid is True
    assert len(records) == 1
    assert err is None

def test_input_contract_csv_parsing():
    raw_csv = "timestamp,device,energy_kwh,duration_minutes\n2026-09-01T10:00:00,hvac,2.5,60"
    is_valid, records, err = InputContract.parse_input_records(raw_csv)
    assert is_valid is True
    assert len(records) == 1

def test_input_contract_empty_dataset():
    is_valid, records, err = InputContract.parse_input_records("")
    assert is_valid is False
    assert err["code"] == "EMPTY_DATASET"

def test_input_contract_negative_energy():
    records = [{"timestamp": "2026-09-01T10:00:00", "energy_kwh": -5.0}]
    is_valid, clean, err = InputContract.validate_records(records)
    assert is_valid is False
    assert err["code"] == "INVALID_ENERGY_VALUE"

def test_input_contract_missing_tariff():
    is_valid, val, err = InputContract.validate_tariff(None)
    assert is_valid is False
    assert err["code"] == "INVALID_TARIFF"

def test_output_contract_formatting():
    res = OutputContract.success("cap", "tool", {"total": 10})
    assert res["status"] == "success"
    assert res["capability"] == "cap"
    assert res["tool"] == "tool"

def test_behavior_contract():
    bc = BehaviorContract()
    assert len(bc.get_allowed_capabilities()) > 0
    assert len(bc.get_allowed_tools()) > 0
