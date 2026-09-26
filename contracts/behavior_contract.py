from typing import Any, Dict, List, Optional
from passport.passport_manager import PassportManager

class BehaviorContract:
    """Dynamic Behavior Contract derived from Agent Passport configuration."""

    def __init__(self, passport_manager: Optional[PassportManager] = None):
        if passport_manager is None:
            self.passport_manager = PassportManager()
        else:
            self.passport_manager = passport_manager

    def get_allowed_capabilities(self) -> List[str]:
        return self.passport_manager.get_capabilities()

    def get_allowed_tools(self) -> List[str]:
        return self.passport_manager.get_tools()

    def is_capability_allowed(self, capability: str) -> bool:
        return capability in self.get_allowed_capabilities()

    def is_tool_allowed(self, tool_name: str) -> bool:
        return tool_name in self.get_allowed_tools()

    def validate_capability_tool_mapping(self, capability: str, tool_name: str) -> bool:
        mapped_tool = self.passport_manager.get_tool_for_capability(capability)
        return mapped_tool == tool_name

    def get_lifecycle_states(self) -> List[str]:
        return [
            "INPUT",
            "REQUEST_VALIDATION",
            "PASSPORT_LOADING",
            "CAPABILITY_VALIDATION",
            "TOOL_DISCOVERY",
            "TOOL_EXECUTION",
            "RESULT_VALIDATION",
            "RESPONSE_GENERATION"
        ]

    def get_provider_boundary_policy(self) -> Dict[str, Any]:
        return {
            "mode": "offline_deterministic",
            "allow_external_failover": False,
            "secret_redaction": True
        }
