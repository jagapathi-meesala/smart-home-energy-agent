import yaml
import json
import jsonschema

with open('schema.json', 'r') as f:
    schema = json.load(f)

agent_data = """
spec_version: "0.1.0"
name: "smart-home-energy-agent"
version: "1.0.0"
description: "A framework-independent, portable AI agent for smart home energy consumption analysis, pattern detection, anomaly detection, cost estimation, recommendations, and reporting."
author: "HiDevs x Lyzr"
tools:
  - energy-consumption-analyzer
  - appliance-energy-analyzer
  - energy-pattern-detector
  - energy-anomaly-detector
  - energy-cost-estimator
  - energy-recommendation
  - energy-report
metadata:
  id: "smart-home-energy-agent-01"
  trust_level: "local_verified"
  portability: "framework_independent"
  execution_mode: "offline_deterministic"
"""

data = yaml.safe_load(agent_data)

try:
    jsonschema.validate(instance=data, schema=schema)
    print("VALID!")
except jsonschema.exceptions.ValidationError as e:
    print("INVALID:", e.message)
