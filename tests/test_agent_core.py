from core.agent_core import AgentCore

def test_agent_core_handle_request_success():
    core = AgentCore()
    data = [
        {"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 3.0}
    ]
    resp = core.handle_request("energy_consumption_analysis", data)
    assert resp["status"] == "success"
    assert resp["tool"] == "energy_consumption_analyzer_tool"
    assert "lifecycle" in resp["metadata"]

def test_agent_core_unknown_capability():
    core = AgentCore()
    resp = core.handle_request("non_existent_capability", [])
    assert resp["status"] == "error"
    assert resp["code"] == "CAPABILITY_NOT_FOUND"
