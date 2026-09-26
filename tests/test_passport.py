from passport.passport_manager import PassportManager

def test_passport_loading():
    mgr = PassportManager()
    assert mgr.get_agent_name() == "smart-home-energy-agent"
    assert mgr.get_agent_id() == "smart-home-energy-agent-01"
    assert mgr.get_version() == "1.0.0"

def test_passport_tools():
    mgr = PassportManager()
    tools = mgr.get_tools()
    assert len(tools) > 0
    assert "energy-consumption-analyzer" in tools

def test_capability_tool_mapping():
    mgr = PassportManager()
    tool_name = mgr.get_tool_for_capability("energy_anomaly_detection")
    assert tool_name == "energy-anomaly-detector"
