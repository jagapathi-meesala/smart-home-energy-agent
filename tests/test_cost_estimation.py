from tools.energy_cost_estimator import EnergyCostEstimatorTool

def test_energy_cost_estimator_valid_tariff():
    tool = EnergyCostEstimatorTool()
    records = [
        {"timestamp": "2026-09-01T10:00:00", "energy_kwh": 10.0}
    ]
    ok, res, err = tool.execute(records, tariff_per_kwh=0.20)
    assert ok is True
    assert res["estimated_cost"] == 2.0
    assert "calculation_explanation" in res

def test_energy_cost_estimator_missing_tariff():
    tool = EnergyCostEstimatorTool()
    records = [
        {"timestamp": "2026-09-01T10:00:00", "energy_kwh": 10.0}
    ]
    ok, res, err = tool.execute(records, tariff_per_kwh=None)
    assert ok is False
    assert err["code"] == "INVALID_TARIFF"
