from verification.hardcoding_audit import HardcodingAudit

def test_hardcoding_audit_pass():
    audit = HardcodingAudit()
    res = audit.verify()
    assert res["status"] == "PASSED"
    assert len(res["findings"]) == 0
