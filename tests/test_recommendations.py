from tools.energy_recommendation import EnergyRecommendationTool

def test_energy_recommendation_tool():
    tool = EnergyRecommendationTool()
    records = [
        {"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 8.0},
        {"timestamp": "2026-09-01T11:00:00", "device": "fridge", "energy_kwh": 0.5}
    ]
    ok, res, err = tool.execute(records)
    assert ok is True
    assert "recommendations" in res
    assert "disclaimer" in res
    assert len(res["recommendations"]) > 0
