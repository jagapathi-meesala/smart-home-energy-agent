from typing import Any, Dict
from adapters.framework_adapter import FrameworkAdapter
from adapters.openai_adapter import OpenAIAdapter

class FrameworkVerifier:
    """Verifies generic framework adapters and optional OpenAI SDK integration boundaries."""

    def verify(self) -> Dict[str, Any]:
        details = []

        # 1. Generic Framework Adapter Structural Verification
        fw_adapter = FrameworkAdapter("generic_verifier")
        boundary_info = fw_adapter.verify_framework_boundary()
        details.append(f"Framework boundary check: {boundary_info['boundary_status']} (Reason: {boundary_info['reason']})")

        # 2. OpenAI Adapter Status
        openai_adapter = OpenAIAdapter()
        sdk_installed = openai_adapter.is_sdk_installed()
        configured = openai_adapter.is_configured()

        details.append(f"OpenAI SDK Installed: {sdk_installed}")
        details.append(f"OpenAI Configured: {configured}")

        if not sdk_installed:
            ext_status = "SKIPPED"
            ext_reason = "SDK_NOT_INSTALLED"
        elif not configured:
            ext_status = "SKIPPED"
            ext_reason = "PROVIDER_NOT_CONFIGURED"
        else:
            ext_status = "READY"
            ext_reason = "CREDENTIALS_PRESENT"

        passed = (boundary_info.get("boundary_status") == "STRUCTURAL_ADAPTER")
        status = "PASSED" if passed else "FAILED"

        return {
            "status": status,
            "verifier": "FrameworkVerifier",
            "structural_verification": "PASSED" if passed else "FAILED",
            "real_external_execution": ext_status,
            "reason": ext_reason,
            "details": details
        }
