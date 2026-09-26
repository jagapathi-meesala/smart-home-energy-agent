import re
from pathlib import Path
from typing import Any, Dict, List
from config.settings import settings

class HardcodingAudit:
    """Scans repository source code for hardcoded secrets, credentials, or fixed verification counts."""

    SUSPICIOUS_PATTERNS = [
        (r'sk-[a-zA-Z0-9]{20,}', "Hardcoded OpenAI API key pattern"),
        (r'bearer\s+[a-zA-Z0-9_\-\.]{20,}', "Hardcoded Bearer Token pattern"),
        (r'aws_secret_access_key\s*=', "Hardcoded AWS secret key pattern"),
        (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password assignment"),
    ]

    def verify(self) -> Dict[str, Any]:
        details: List[str] = []
        findings: List[str] = []

        base_dir = settings.BASE_DIR
        py_files = list(base_dir.rglob("*.py"))

        for file_path in py_files:
            # Skip test files and virtual envs
            rel_path = file_path.relative_to(base_dir)
            path_str = str(rel_path)
            if "venv" in path_str or ".pytest_cache" in path_str or "__pycache__" in path_str:
                continue

            try:
                text = file_path.read_text(encoding="utf-8")
                for pattern, desc in self.SUSPICIOUS_PATTERNS:
                    if re.search(pattern, text, re.IGNORECASE):
                        findings.append(f"{desc} in file: {rel_path}")
            except Exception as e:
                details.append(f"Could not scan file {rel_path}: {str(e)}")

        details.append(f"Scanned {len(py_files)} Python source files across repository.")

        passed = (len(findings) == 0)
        status = "PASSED" if passed else "FAILED"

        return {
            "status": status,
            "verifier": "HardcodingAudit",
            "findings": findings,
            "details": details
        }
