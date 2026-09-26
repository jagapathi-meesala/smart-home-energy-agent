# Smart Home Energy Agent (`smart-home-energy-agent`)

> A portable, framework-independent, offline-first AI agent for smart home energy consumption analysis, pattern detection, statistical anomaly detection, cost estimation, recommendations, and structured reporting.

---

## Overview

**Smart Home Energy Agent** (`smart-home-energy-agent`) is a portable agent designed according to the HiDevs x Lyzr Agent Passport specification (`spec_version: "0.1.0"`). It processes generic household energy consumption datasets (in JSON or CSV formats) using deterministic statistical calculations without external cloud API dependencies or real smart hardware integrations.

- **Agent Name**: `smart-home-energy-agent`
- **Agent ID**: `smart-home-energy-agent-01`
- **Version**: `1.0.0`
- **Execution Mode**: `offline_deterministic`

---

## Architecture

```
External Framework
        |
        v
Framework Adapter
        |
        v
Portable Adapter
        |
        v
    AgentCore  <--- Single Source of Truth
        |
        v
 ExecutionEngine
        |
        +---- PassportManager
        |
        +---- ToolRegistry
        |
        +---- BehaviorContract
        |
        v
   Domain Tools
        |
        v
 Structured Result
```

---

## Capabilities

The agent dynamically loads capabilities from `agent.yaml`:

1. `energy_consumption_analysis`: Total, average, peak, minimum, and summary statistics.
2. `appliance_energy_analysis`: Consumption breakdown and percentage contribution by appliance/category.
3. `energy_pattern_detection`: Hourly, daily, and weekday vs. weekend temporal distributions.
4. `energy_anomaly_detection`: Transparent statistical anomaly scoring (Z-score, IQR, threshold) with explanations.
5. `energy_cost_estimation`: Financial estimates calculated via `energy_kwh × tariff_per_kwh`.
6. `energy_saving_recommendation`: Automated efficiency recommendations derived from statistics.
7. `energy_reporting`: Synthesis of complete structured JSON energy reports.

---

## Tools

Registered deterministically in `ToolRegistry`:

- `energy_consumption_analyzer_tool`
- `appliance_energy_analyzer_tool`
- `energy_pattern_detector_tool`
- `energy_anomaly_detector_tool`
- `energy_cost_estimator_tool`
- `energy_recommendation_tool`
- `energy_report_tool`

---

## Input Format

Accepts generic JSON or CSV datasets. Example record format:

```json
{
  "timestamp": "2026-09-01T10:00:00",
  "device": "hvac",
  "energy_kwh": 1.25,
  "duration_minutes": 60,
  "tariff_per_kwh": 0.15
}
```

---

## Output Format

Structured JSON output schema:

```json
{
  "status": "success",
  "capability": "energy_consumption_analysis",
  "tool": "energy_consumption_analyzer_tool",
  "result": { ... },
  "metadata": {
    "agent_id": "smart-home-energy-agent-01",
    "timestamp": "2026-09-26T18:14:43Z"
  }
}
```

---

## Installation

```bash
cd smart-home-energy-agent
pip install -r requirements.txt
```

---

## Usage

```python
from adapters.portable_adapter import PortableAdapter

adapter = PortableAdapter()
response = adapter.execute(
    capability="energy_consumption_analysis",
    input_data=[
        {"timestamp": "2026-09-01T10:00:00", "device": "fridge", "energy_kwh": 0.4, "duration_minutes": 60}
    ]
)
print(response)
```

---

## Demo

Run the offline synthetic demo:

```bash
python scripts/demo.py
```

---

## Testing

Run all unit and integration tests using pytest:

```bash
pytest
```

---

## Verification & Audits

Execute the comprehensive audit and verification suite:

```bash
python scripts/run_all_audits.py
```

Or run agent validation:

```bash
python scripts/validate_agent.py
```

Audits verified:
1. `Passport Trust Verification`
2. `Portability Verification`
3. `Framework Verification`
4. `Security Audit`
5. `Hardcoding Audit`
6. `HiDevs Readiness Audit`

---

## Portability & Framework Integration

The agent is framework-agnostic. `PortableAdapter` operates 100% locally. Generic `FrameworkAdapter` and optional `OpenAIAdapter` provide clean boundaries for multi-agent integration. If external API credentials are missing, the agent gracefully reports `PROVIDER_NOT_CONFIGURED` without failing core capabilities.

---

## Limitations

- The agent is purely an analytical assistant and does not control physical electrical hardware.
- Recommendations are algorithmically generated suggestions and do not constitute certified electrical engineering advice.

---

## License

MIT License.
