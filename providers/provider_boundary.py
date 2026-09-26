from typing import Any, Dict, Optional
from adapters.openai_adapter import OpenAIAdapter
from adapters.portable_adapter import PortableAdapter

class ProviderBoundary:
    """Boundary isolating local deterministic execution from optional external LLM providers."""

    EXECUTION_MODE_LOCAL = "LOCAL_DETERMINISTIC_EXECUTION"
    EXECUTION_MODE_EXTERNAL = "OPTIONAL_EXTERNAL_PROVIDER_EXECUTION"

    def __init__(self):
        self.local_adapter = PortableAdapter()
        self.openai_adapter = OpenAIAdapter()

    def execute_capability(
        self,
        capability: str,
        input_payload: Any,
        prefer_external: bool = False,
        **kwargs
    ) -> Dict[str, Any]:

        if prefer_external:
            if self.openai_adapter.is_configured() and self.openai_adapter.is_sdk_installed():
                ext_response = self.openai_adapter.execute(capability, input_payload)
                if ext_response.get("status") == "success":
                    return {
                        "execution_mode": self.EXECUTION_MODE_EXTERNAL,
                        "response": ext_response
                    }

        # Fallback / Default: Local deterministic engine
        local_response = self.local_adapter.execute(capability, input_payload, **kwargs)
        return {
            "execution_mode": self.EXECUTION_MODE_LOCAL,
            "response": local_response
        }
