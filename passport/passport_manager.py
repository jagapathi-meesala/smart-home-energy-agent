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
        return self.data.get("metadata", {}).get("id", "smart-home-energy-agent-01")

    def get_version(self) -> str:
        return self.data.get("version", "1.0.0")

    def get_description(self) -> str:
        return self.data.get("description", "")

    def get_tools(self) -> List[str]:
        tools = self.data.get("tools", [])
        return [t for t in tools if isinstance(t, str)]

    def _get_capability_tool_mapping(self) -> Dict[str, str]:
        return {
            "energy_consumption_analysis": "energy-consumption-analyzer",
            "appliance_energy_analysis": "appliance-energy-analyzer",
            "energy_pattern_detection": "energy-pattern-detector",
            "energy_anomaly_detection": "energy-anomaly-detector",
            "energy_cost_estimation": "energy-cost-estimator",
            "energy_saving_recommendation": "energy-recommendation",
            "energy_reporting": "energy-report"
        }

    def get_capabilities(self) -> List[str]:
        return list(self._get_capability_tool_mapping().keys())

    def get_tool_for_capability(self, capability_name: str) -> Optional[str]:
        # Legacy capability routing is not strictly needed since OpenGAP uses tools directly.
        # But we preserve the interface returning a mapped tool string for compatibility.
        return self._get_capability_tool_mapping().get(capability_name)

    def validate_capability(self, capability_name: str) -> bool:
        return self.get_tool_for_capability(capability_name) is not None

    def validate_tool(self, tool_name: str) -> bool:
        return tool_name in self.get_tools()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "spec_version": self.data.get("spec_version"),
            "agent_id": self.get_agent_id(),
            "metadata": self.data.get("metadata", {}),
            "tools_count": len(self.get_tools())
        }
