import os
from typing import Any, Dict, Optional
from config.settings import settings

class OpenAIAdapter:
    """Optional OpenAI SDK integration adapter with strict fallback reporting."""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    @staticmethod
    def is_sdk_installed() -> bool:
        try:
            import openai  # noqa: F401
            return True
        except ImportError:
            return False

    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def execute(self, capability: str, input_payload: Any) -> Dict[str, Any]:
        if not self.is_sdk_installed():
            return {
                "status": "awaiting_tools",
                "code": "SDK_NOT_INSTALLED",
                "reason": "OpenAI Python package is not installed in the environment.",
                "capability": capability
            }

        if not self.is_configured():
            return {
                "status": "awaiting_tools",
                "code": "PROVIDER_NOT_CONFIGURED",
                "reason": "OPENAI_API_KEY environment variable is missing or empty.",
                "capability": capability
            }

        # If SDK is installed and key is present, attempt call safely (or handle mock/real call)
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            # Standard light health ping or prompt response
            completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a smart home energy analyzer assistant."},
                    {"role": "user", "content": f"Analyze capability request: {capability}"}
                ]
            )
            return {
                "status": "success",
                "provider": "openai",
                "model": self.model,
                "result": completion.choices[0].message.content
            }
        except Exception as e:
            # Redact API keys from exception message
            err_msg = str(e)
            if self.api_key:
                err_msg = err_msg.replace(self.api_key, "[REDACTED]")

            return {
                "status": "error",
                "code": "PROVIDER_EXECUTION_FAILED",
                "reason": f"OpenAI API execution failed: {err_msg}",
                "capability": capability
            }
