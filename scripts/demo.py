#!/usr/bin/env python3
import json
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from adapters.portable_adapter import PortableAdapter

def run_demo():
    print("============================================================")
    print(" SMART HOME ENERGY AGENT - OFFLINE SYNTHETIC DEMO")
    print("============================================================\n")

    # Construct synthetic demonstration dataset
    # NOTE: THIS DATASET IS DEMO DATA (SYNTHETIC BENCHMARK DATA)
    synthetic_demo_dataset = [
        {"timestamp": "2026-09-01T08:00:00", "device": "hvac", "energy_kwh": 2.10, "duration_minutes": 60, "tariff_per_kwh": 0.15},
        {"timestamp": "2026-09-01T09:00:00", "device": "refrigerator", "energy_kwh": 0.35, "duration_minutes": 60, "tariff_per_kwh": 0.15},
        {"timestamp": "2026-09-01T10:00:00", "device": "lighting", "energy_kwh": 0.15, "duration_minutes": 60, "tariff_per_kwh": 0.15},
        {"timestamp": "2026-09-01T11:00:00", "device": "ev_charger", "energy_kwh": 7.20, "duration_minutes": 60, "tariff_per_kwh": 0.15},
        {"timestamp": "2026-09-01T12:00:00", "device": "hvac", "energy_kwh": 2.40, "duration_minutes": 60, "tariff_per_kwh": 0.15},
        {"timestamp": "2026-09-01T13:00:00", "device": "dishwasher", "energy_kwh": 1.20, "duration_minutes": 60, "tariff_per_kwh": 0.15},
        # High consumption spike / anomaly simulation record
        {"timestamp": "2026-09-01T14:00:00", "device": "hvac", "energy_kwh": 8.90, "duration_minutes": 60, "tariff_per_kwh": 0.15},
        {"timestamp": "2026-09-01T15:00:00", "device": "refrigerator", "energy_kwh": 0.38, "duration_minutes": 60, "tariff_per_kwh": 0.15}
    ]

    adapter = PortableAdapter()

    capabilities = [
        "energy_consumption_analysis",
        "appliance_energy_analysis",
        "energy_pattern_detection",
        "energy_anomaly_detection",
        "energy_cost_estimation",
        "energy_saving_recommendation",
        "energy_reporting"
    ]

    results = {}
    for cap in capabilities:
        print(f"Executing Capability: {cap}...")
        resp = adapter.execute(cap, synthetic_demo_dataset, tariff_per_kwh=0.15)
        results[cap] = resp

    print("\n------------------------------------------------------------")
    print(" DEMO EXECUTION COMPLETE - STRUCTURED JSON SUMMARY REPORT")
    print("------------------------------------------------------------\n")
    print(json.dumps(results["energy_reporting"], indent=2))

if __name__ == "__main__":
    run_demo()
