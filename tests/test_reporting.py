from tools.energy_report import EnergyReportTool

def test_energy_report_tool():
    tool = EnergyReportTool()
    records = [
        {"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 3.0, "tariff_per_kwh": 0.15},
        {"timestamp": "2026-09-01T11:00:00", "device": "lighting", "energy_kwh": 0.5, "tariff_per_kwh": 0.15}
    ]
    ok, report, err = tool.execute(records)
    assert ok is True
    assert "summary" in report
    assert "consumption_analysis" in report
    assert "appliance_breakdown" in report
    assert "detected_patterns" in report
    assert "detected_anomalies" in report
    assert "estimated_cost" in report
    assert "recommendations" in report
    assert "limitations" in report
