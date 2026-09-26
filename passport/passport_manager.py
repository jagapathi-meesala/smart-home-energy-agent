import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional
from config.settings import settings
from passport.passport_schema import PassportSchemaValidator

class PassportManager:
    """Manages Agent Passport loading, dynamic inspection, and integrity checks."""

    def __init__(self, passport_path: Optional[Path] = None):
        self.passport_path = passport_path or settings.PASSPORT_PATH
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if not Path(self.passport_path).exists():
            raise FileNotFoundError(f"Agent Passport file not found at: {self.passport_path}")

        with open(self.passport_path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f)

        is_valid, errors = PassportSchemaValidator.validate(raw_data)
        if not is_valid:
            raise ValueError(f"Invalid Agent Passport schema in {self.passport_path}: {'; '.join(errors)}")

        self.data = raw_data

    def get_agent_name(self) -> str:
        return self.data.get("name", "smart-home-energy-agent")

    def get_agent_id(self) -> str:
        return self.data.get("id", "smart-home-energy-agent-01")

    def get_version(self) -> str:
        return self.data.get("version", "1.0.0")

    def get_description(self) -> str:
        return self.data.get("description", "")

    def get_capabilities(self) -> List[str]:
        caps = self.data.get("capabilities", [])
        return [c["name"] for c in caps if isinstance(c, dict) and "name" in c]

    def get_tools(self) -> List[str]:
        tools = self.data.get("tools", [])
        return [t["name"] for t in tools if isinstance(t, dict) and "name" in t]

    def get_tool_for_capability(self, capability_name: str) -> Optional[str]:
        tools = self.data.get("tools", [])
        for tool in tools:
            if isinstance(tool, dict) and tool.get("capability") == capability_name:
                return tool.get("name")
        return None

    def validate_capability(self, capability_name: str) -> bool:
        return capability_name in self.get_capabilities()

    def validate_tool(self, tool_name: str) -> bool:
        return tool_name in self.get_tools()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "spec_version": self.data.get("spec_version"),
            "agent_id": self.get_agent_id(),
            "passport": self.data.get("passport", {}),
            "capabilities_count": len(self.get_capabilities()),
            "tools_count": len(self.get_tools())
        }
