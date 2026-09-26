from tools.tool_registry import ToolRegistry, BaseTool
from tools.energy_consumption_analyzer import EnergyConsumptionAnalyzerTool

def test_tool_registry_registration_and_lookup():
    registry = ToolRegistry()
    tool = EnergyConsumptionAnalyzerTool()
    registry.register(tool)

    assert registry.exists("energy_consumption_analyzer_tool")
    assert registry.get("energy_consumption_analyzer_tool") == tool
    assert "energy_consumption_analyzer_tool" in registry.list()

def test_tool_registry_execute():
    registry = ToolRegistry()
    tool = EnergyConsumptionAnalyzerTool()
    registry.register(tool)

    records = [{"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 2.0}]
    ok, result, err = registry.execute("energy_consumption_analyzer_tool", records)
    assert ok is True
    assert result["total_energy_kwh"] == 2.0
