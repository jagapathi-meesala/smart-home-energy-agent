from tools.tool_registry import ToolRegistry, BaseTool
from tools.energy_consumption_analyzer import EnergyConsumptionAnalyzerTool

def test_tool_registry_registration_and_lookup():
    registry = ToolRegistry()
    tool = EnergyConsumptionAnalyzerTool()
    registry.register(tool)

    assert registry.exists("energy-consumption-analyzer")
    assert registry.get("energy-consumption-analyzer") == tool
    assert "energy-consumption-analyzer" in registry.list()

def test_tool_registry_execute():
    registry = ToolRegistry()
    tool = EnergyConsumptionAnalyzerTool()
    registry.register(tool)

    records = [{"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 2.0}]
    ok, result, err = registry.execute("energy-consumption-analyzer", records)
    assert ok is True
    assert result["total_energy_kwh"] == 2.0
