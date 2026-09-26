from tools.energy_pattern_detector import EnergyPatternDetectorTool

def test_energy_pattern_detector_tool():
    tool = EnergyPatternDetectorTool()
    records = [
        {"timestamp": "2026-09-01T08:00:00", "device": "hvac", "energy_kwh": 2.0},  # Tuesday (weekday)
        {"timestamp": "2026-09-01T14:00:00", "device": "hvac", "energy_kwh": 5.0},
        {"timestamp": "2026-09-05T10:00:00", "device": "hvac", "energy_kwh": 1.0}   # Saturday (weekend)
    ]
    ok, res, err = tool.execute(records)
    assert ok is True
    assert "hourly_patterns" in res
    assert res["weekday_vs_weekend"]["weekday_total_kwh"] == 7.0
    assert res["weekday_vs_weekend"]["weekend_total_kwh"] == 1.0
