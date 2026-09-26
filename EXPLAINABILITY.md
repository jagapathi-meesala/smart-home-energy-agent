# EXPLAINABILITY - SmartHomeEnergyAgent Architectural Transparency

## Purpose
The purpose of `SmartHomeEnergyAgent` is to deliver fully transparent, deterministic, and verifiable energy analytics for smart home datasets. It provides a standardized specification for analyzing household electricity consumption, identifying high usage devices, detecting statistical anomalies, estimating costs, and proposing efficiency recommendations without relying on black-box machine learning.

## Inputs and Data Sources
The agent processes tabular energy consumption records provided in JSON or CSV formats. Each record contains attributes such as ISO timestamps, appliance/device names, duration in minutes, and numeric energy consumption measured in kilowatt-hours (kWh), along with optional electricity tariff rates.

## Decision and Reasoning
The agent reaches analytical conclusions through transparent, deterministic mathematical formulas and statistical algorithms. For energy anomaly detection, the agent applies standard Z-score analysis ($Z = \frac{x - \mu}{\sigma}$) or Interquartile Range ($IQR = Q_3 - Q_1$) thresholds to identify records exceeding statistical control bounds and provides an explicit mathematical justification for each flag. For cost estimation, financial figures are calculated directly via the formula: `estimated_cost = energy_kwh × tariff_per_kwh`.

## Tools and Capabilities
The agent's functionality is partitioned into seven deterministic domain tools managed by a dynamic ToolRegistry and derived from the Agent Passport. These tools include consumption analysis, appliance category breakdown, temporal pattern detection, statistical anomaly detection, cost estimation, energy-saving recommendation generation, and structured report synthesis.

## Limitations and Constraints
The system operates exclusively as an analytical energy assistant and does not possess direct hardware control or physical intervention capabilities over electrical circuits. Recommendations are generated algorithmically from statistical metrics and represent analytical suggestions rather than certified electrical engineering advice or official utility billing invoices.

## Portability
The core execution engine (`AgentCore`) is completely framework-independent and requires no internet access, external API keys, or cloud infrastructure. It can operate 100% offline in any local Python 3.10+ environment or integrate seamlessly into multi-agent systems via lightweight adapters.

## Verification
System integrity and trust are validated through a dynamic verification suite comprising six automated audit modules. These modules verify passport schema compliance, core engine portability, framework adapter boundaries, security posture, zero hardcoding of secret credentials or fixed assumptions, and overall HiDevs platform readiness.

## Failure Handling
When presented with malformed payloads, negative consumption values, empty datasets, or missing parameters, the agent rejects the request gracefully without throwing unhandled exceptions. It returns structured JSON error responses containing explicit error codes (e.g., `INVALID_INPUT`, `EMPTY_DATASET`, `MISSING_FIELD`, `INVALID_TARIFF`) and detailed diagnostic messages.

## Expected Output
All tools and execution routines produce predictable, schema-compliant JSON outputs detailing statistics, category distributions, anomaly explanations, and recommendations. The final energy report consolidates all analytical sections into a unified JSON structure suitable for programmatic downstream consumption.
