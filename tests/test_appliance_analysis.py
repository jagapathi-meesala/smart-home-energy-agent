from tools.appliance_energy_analyzer import ApplianceEnergyAnalyzerTool

def test_appliance_energy_analyzer_arbitrary_categories():
    tool = ApplianceEnergyAnalyzerTool()
    records = [
        {"timestamp": "2026-09-01T10:00:00", "device": "custom_gadget_a", "energy_kwh": 6.0},
        {"timestamp": "2026-09-01T11:00:00", "device": "custom_gadget_b", "energy_kwh": 4.0}
    ]
    ok, res, err = tool.execute(records)
    assert ok is True
    breakdown = res["appliance_breakdown"]
    assert "custom_gadget_a" in breakdown
    assert breakdown["custom_gadget_a"]["percentage_contribution"] == 60.0
    assert breakdown["custom_gadget_b"]["percentage_contribution"] == 40.0
