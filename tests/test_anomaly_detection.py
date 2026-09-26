from tools.energy_anomaly_detector import EnergyAnomalyDetectorTool

def test_energy_anomaly_detector_z_score():
    tool = EnergyAnomalyDetectorTool()
    records = [
        {"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 1.0},
        {"timestamp": "2026-09-01T11:00:00", "device": "hvac", "energy_kwh": 1.1},
        {"timestamp": "2026-09-01T12:00:00", "device": "hvac", "energy_kwh": 1.0},
        {"timestamp": "2026-09-01T13:00:00", "device": "hvac", "energy_kwh": 1.2},
        {"timestamp": "2026-09-01T14:00:00", "device": "hvac", "energy_kwh": 15.0}  # Anomaly spike
    ]
    ok, res, err = tool.execute(records, method="z_score", z_threshold=1.5)
    assert ok is True
    assert res["anomaly_count"] >= 1
    anom = res["anomalies"][0]
    assert anom["value_kwh"] == 15.0
    assert "explanation" in anom
