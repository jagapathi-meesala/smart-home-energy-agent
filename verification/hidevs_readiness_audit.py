from pathlib import Path
from typing import Any, Dict, List
from config.settings import settings
from passport.passport_manager import PassportManager

class HiDevsReadinessAudit:
    """Audits repository completeness, required root files, EXPLAINABILITY headings, and HiDevs passport readiness."""

    REQUIRED_ROOT_FILES = [
        "agent.yaml",
        "SOUL.md",
        "DUTIES.md",
        "EXPLAINABILITY.md",
        "README.md",
        "requirements.txt",
        ".env.example",
        ".gitignore"
    ]

    REQUIRED_EXPLAINABILITY_HEADINGS = [
        "## Purpose",
        "## Inputs and Data Sources",
        "## Decision and Reasoning",
        "## Tools and Capabilities",
        "## Limitations and Constraints",
        "## Portability",
        "## Verification",
        "## Failure Handling",
        "## Expected Output"
    ]

    def verify(self) -> Dict[str, Any]:
        details: List[str] = []
        issues: List[str] = []

        base_dir = settings.BASE_DIR

        # 1. Root Files Check
        for fname in self.REQUIRED_ROOT_FILES:
            fpath = base_dir / fname
            if not fpath.exists():
                issues.append(f"Missing required root file: '{fname}'.")
            elif fpath.stat().st_size == 0:
                issues.append(f"Required root file '{fname}' is empty.")
            else:
                details.append(f"Root file '{fname}' verified present and non-empty.")

        # 2. Agent Passport Check
        try:
            mgr = PassportManager()
            agent_info = mgr.get_agent_info()
            if mgr.data.get("spec_version") != "0.1.0":
                issues.append(f"agent.yaml spec_version is '{mgr.data.get('spec_version')}', expected '0.1.0'.")

            root_name = mgr.data.get("name")
            if root_name != "smart-home-energy-agent":
                issues.append(f"Root-level agent name is '{root_name}', expected 'smart-home-energy-agent'.")

            root_ver = mgr.data.get("version")
            if root_ver != "1.0.0":
                issues.append(f"Root-level version is '{root_ver}', expected '1.0.0'.")

            root_desc = mgr.data.get("description")
            if not root_desc or not str(root_desc).strip():
                issues.append("Root-level description is missing in agent.yaml.")

            if agent_info.get("name") != "smart-home-energy-agent":
                issues.append(f"Agent section name is '{agent_info.get('name')}', expected 'smart-home-energy-agent'.")

            caps = mgr.get_capabilities()
            tools = mgr.get_tools()
            if not caps or not tools:
                issues.append("Agent Passport contains empty capabilities or tools list.")
            else:
                details.append(f"Passport capabilities ({len(caps)}) and tools ({len(tools)}) validated.")
        except Exception as e:
            issues.append(f"PassportManager loading error: {str(e)}")

        # 3. EXPLAINABILITY Headings & Content Check
        explainability_path = base_dir / "EXPLAINABILITY.md"
        if explainability_path.exists():
            exp_text = explainability_path.read_text(encoding="utf-8")
            for h in self.REQUIRED_EXPLAINABILITY_HEADINGS:
                if h not in exp_text:
                    issues.append(f"EXPLAINABILITY.md missing required section heading: '{h}'.")
                else:
                    details.append(f"Heading '{h}' present in EXPLAINABILITY.md.")

        passed = (len(issues) == 0)
        status = "PASSED" if passed else "FAILED"

        return {
            "status": status,
            "verifier": "HiDevsReadinessAudit",
            "issues": issues,
            "details": details
        }
