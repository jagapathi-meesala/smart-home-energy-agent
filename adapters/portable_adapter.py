from typing import Any, Dict, Optional
from core.agent_core import AgentCore

class PortableAdapter:
    """Framework-independent portable adapter for offline local execution."""

    def __init__(self, passport_path: Optional[str] = None):
        self.agent_core = AgentCore(passport_path)

    def execute(self, capability: str, input_data: Any, **kwargs) -> Dict[str, Any]:
        """Directly delegates execution to AgentCore without external framework overhead."""
        return self.agent_core.handle_request(capability=capability, input_payload=input_data, **kwargs)

    def get_capabilities(self) -> list:
        return self.agent_core.passport_manager.get_capabilities()

    def get_tools(self) -> list:
        return self.agent_core.passport_manager.get_tools()
