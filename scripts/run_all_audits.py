#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_all():
    print("============================================================")
    print(" RUNNING ALL TEST SUITES AND VERIFICATION AUDITS")
    print("============================================================\n")

    # 1. Run Pytest
    print(">>> 1. Running Pytest Suite...")
    pytest_res = subprocess.run([sys.executable, "-m", "pytest", str(BASE_DIR / "tests")], cwd=str(BASE_DIR))
    if pytest_res.returncode != 0:
        print("\n[ERROR] Pytest execution failed.")
        sys.exit(pytest_res.returncode)

    print("\n>>> Pytest execution PASSED.\n")

    # 2. Run Validation Script
    print(">>> 2. Running Agent Validation Script...")
    val_res = subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "validate_agent.py")], cwd=str(BASE_DIR))
    if val_res.returncode != 0:
        print("\n[ERROR] Agent Validation Script failed.")
        sys.exit(val_res.returncode)

    print("\n============================================================")
    print(" ALL TESTS AND AUDITS PASSED SUCCESSFULLY!")
    print("============================================================")

if __name__ == "__main__":
    run_all()
