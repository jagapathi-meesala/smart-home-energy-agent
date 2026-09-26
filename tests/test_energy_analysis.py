from tools.energy_consumption_analyzer import EnergyConsumptionAnalyzerTool

def test_energy_consumption_analyzer_tool():
    tool = EnergyConsumptionAnalyzerTool()
    records = [
        {"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 2.0},
        {"timestamp": "2026-09-01T11:00:00", "device": "fridge", "energy_kwh": 0.5},
        {"timestamp": "2026-09-01T12:00:00", "device": "hvac", "energy_kwh": 3.5}
    ]
    ok, res, err = tool.execute(records)
    assert ok is True
    assert res["total_energy_kwh"] == 6.0
    assert res["average_energy_kwh"] == 2.0
    assert res["peak_consumption"]["energy_kwh"] == 3.5
    assert res["minimum_consumption"]["energy_kwh"] == 0.5
