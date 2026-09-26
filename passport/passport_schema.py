from typing import Any, Dict, List, Tuple

class PassportSchemaValidator:
    """Validates Agent Passport (agent.yaml) schema consistency."""

    REQUIRED_ROOT_KEYS = ["spec_version", "agent", "capabilities", "tools", "passport"]
    REQUIRED_AGENT_KEYS = ["name", "id", "version"]

    @classmethod
    def validate(cls, passport_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        if not isinstance(passport_data, dict):
            return False, ["Passport root must be a YAML dictionary mapping."]

        for key in cls.REQUIRED_ROOT_KEYS:
            if key not in passport_data:
                errors.append(f"Missing required root key: '{key}'.")

        if errors:
            return False, errors

        # Spec version check
        if passport_data.get("spec_version") != "0.1.0":
            errors.append(f"Invalid spec_version: expected '0.1.0', got '{passport_data.get('spec_version')}'.")

        # Agent section check
        agent_sec = passport_data.get("agent", {})
        if not isinstance(agent_sec, dict):
            errors.append("'agent' section must be a dictionary.")
        else:
            for ak in cls.REQUIRED_AGENT_KEYS:
                if ak not in agent_sec or not str(agent_sec[ak]).strip():
                    errors.append(f"Missing required key in 'agent': '{ak}'.")

            # Validate agent name format: lowercase, hyphenated, starts with letter
            name = agent_sec.get("name", "")
            if not name or not name[0].isalpha() or name != name.lower() or " " in name:
                errors.append(f"Agent name '{name}' must be lowercase, hyphenated, and start with a letter.")

        # Capabilities check
        capabilities = passport_data.get("capabilities", [])
        if not isinstance(capabilities, list) or len(capabilities) == 0:
            errors.append("Capabilities section must be a non-empty list.")
        else:
            for idx, cap in enumerate(capabilities):
                if not isinstance(cap, dict) or "name" not in cap:
                    errors.append(f"Capability at index {idx} must be a dictionary with a 'name' field.")

        # Tools check
        tools = passport_data.get("tools", [])
        if not isinstance(tools, list) or len(tools) == 0:
            errors.append("Tools section must be a non-empty list.")
        else:
            for idx, tool in enumerate(tools):
                if not isinstance(tool, dict) or "name" not in tool:
                    errors.append(f"Tool at index {idx} must be a dictionary with a 'name' field.")

        return (len(errors) == 0), errors
