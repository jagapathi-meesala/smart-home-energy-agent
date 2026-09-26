from typing import Any, Dict, List, Tuple

class PassportSchemaValidator:
    """Validates Agent Passport (agent.yaml) schema consistency."""

    REQUIRED_ROOT_KEYS = ["spec_version", "name", "version", "description", "tools", "metadata"]

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

        # Root name check
        root_name = passport_data.get("name", "")
        if not root_name or not root_name[0].isalpha() or root_name != root_name.lower() or " " in root_name:
            errors.append(f"Root-level agent name '{root_name}' must be lowercase, hyphenated, and start with a letter.")

        # Root version check
        root_ver = passport_data.get("version", "")
        if not root_ver or not str(root_ver).strip():
            errors.append("Root-level version is required.")

        # Root description check
        root_desc = passport_data.get("description", "")
        if not root_desc or not str(root_desc).strip():
            errors.append("Root-level description is required.")

        # Metadata id check
        metadata_sec = passport_data.get("metadata", {})
        if not isinstance(metadata_sec, dict):
            errors.append("'metadata' section must be a dictionary.")
        else:
            root_id = metadata_sec.get("id", "")
            if not root_id or not str(root_id).strip():
                errors.append("Metadata 'id' is required.")

        # Tools check
        tools = passport_data.get("tools", [])
        if not isinstance(tools, list) or len(tools) == 0:
            errors.append("Tools section must be a non-empty list.")
        else:
            for idx, tool in enumerate(tools):
                if not isinstance(tool, str) or not tool.strip():
                    errors.append(f"Tool at index {idx} must be a non-empty string.")

        return (len(errors) == 0), errors
