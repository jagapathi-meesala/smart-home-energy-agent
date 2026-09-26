from adapters.portable_adapter import PortableAdapter
from verification.portability_verifier import PortabilityVerifier

def test_portable_adapter_offline_execution():
    adapter = PortableAdapter()
    records = [{"timestamp": "2026-09-01T10:00:00", "device": "hvac", "energy_kwh": 2.0}]
    resp = adapter.execute("energy_consumption_analysis", records)
    assert resp["status"] == "success"

def test_portability_verifier():
    pv = PortabilityVerifier()
    res = pv.verify()
    assert res["status"] == "PASSED"
    assert res["offline_execution"] is True
