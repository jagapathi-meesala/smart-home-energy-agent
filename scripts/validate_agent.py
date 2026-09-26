#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from verification.framework_verifier import FrameworkVerifier
from verification.hardcoding_audit import HardcodingAudit
from verification.hidevs_readiness_audit import HiDevsReadinessAudit
from verification.passport_trust_verifier import PassportTrustVerifier
from verification.portability_verifier import PortabilityVerifier
from verification.security_audit import SecurityAudit

def validate():
    print("============================================================")
    print(" SMART HOME ENERGY AGENT - AUTOMATED VALIDATION SUITE")
    print("============================================================\n")

    verifiers = [
        ("Passport Trust Verification", PassportTrustVerifier()),
        ("Portability Verification", PortabilityVerifier()),
        ("Framework Verification", FrameworkVerifier()),
        ("Security Audit", SecurityAudit()),
        ("Hardcoding Audit", HardcodingAudit()),
        ("HiDevs Readiness Audit", HiDevsReadinessAudit())
    ]

    summary = {}
    all_passed = True

    for name, v in verifiers:
        res = v.verify()
        status = res.get("status", "UNKNOWN")
        summary[name] = status
        print(f"[{status}] {name}")
        if status != "PASSED":
            all_passed = False
            for detail in res.get("details", []) + res.get("issues", []) + res.get("findings", []):
                print(f"   - {detail}")

    print("\n------------------------------------------------------------")
    print(f"FINAL AUDIT SUMMARY STATUS: {'ALL AUDITS PASSED' if all_passed else 'AUDIT FAILURES DETECTED'}")
    print("------------------------------------------------------------\n")
    print(json.dumps(summary, indent=2))

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    validate()
