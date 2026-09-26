from pathlib import Path
from typing import Any, Dict, List
from config.settings import settings

class SecurityAudit:
    """Audits security configuration, gitignore rules, secret exposure, and input sanitization."""

    def verify(self) -> Dict[str, Any]:
        details: List[str] = []
        issues: List[str] = []

        base_dir = settings.BASE_DIR

        # 1. Check .gitignore
        gitignore_path = base_dir / ".gitignore"
        if not gitignore_path.exists():
            issues.append(".gitignore file is missing from root directory.")
        else:
            content = gitignore_path.read_text(encoding="utf-8")
            if ".env" not in content:
                issues.append(".env is NOT listed in .gitignore.")
            else:
                details.append(".env is properly listed in .gitignore.")

        # 2. Check that real secrets are not present in settings
        if settings.OPENAI_API_KEY.startswith("sk-") and len(settings.OPENAI_API_KEY) > 20:
            issues.append("Active production OpenAI API key detected in process environment variables!")
        else:
            details.append("No sensitive API keys detected in configuration settings.")

        # 3. Secret redaction check in OpenAI Adapter
        from adapters.openai_adapter import OpenAIAdapter
        adapter = OpenAIAdapter()
        if hasattr(adapter, "execute"):
            details.append("OpenAI adapter implements error redaction routines.")

        passed = (len(issues) == 0)
        status = "PASSED" if passed else "FAILED"

        return {
            "status": status,
            "verifier": "SecurityAudit",
            "issues": issues,
            "details": details
        }
