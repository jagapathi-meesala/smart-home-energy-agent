# DUTIES - Operational Responsibilities of SmartHomeEnergyAgent

`SmartHomeEnergyAgent` performs the following primary duties across its execution lifecycle:

## 1. Input Acceptance & Dataset Ingestion
- Accept generic energy dataset records supplied in JSON or CSV format.
- Support arbitrary appliance names and categories dynamically without hardcoding device schemas.

## 2. Dynamic Input Validation
- Validate presence of mandatory fields (e.g., `timestamp`, `energy_kwh`, `duration_minutes`).
- Enforce strict numeric data integrity (reject negative energy values or malformed non-numeric values).
- Validate timestamp formats and detect empty datasets or malformed payloads, returning structured error responses (`INVALID_INPUT`, `EMPTY_DATASET`, `MALFORMED_DATA`).

## 3. Energy Consumption Analysis
- Compute total energy consumption in kilowatt-hours (kWh).
- Compute average, peak, and minimum consumption values across the dataset.
- Calculate consumption metrics and statistical distributions across recorded time intervals.

## 4. Appliance & Category Breakdown
- Group records dynamically by device/appliance category.
- Calculate total kWh and percentage contribution per category.
- Rank highest-consumption appliance categories and summarize usage statistics.

## 5. Temporal Pattern Detection
- Compute hourly consumption distributions across a 24-hour day.
- Analyze daily consumption variations and contrast weekday versus weekend energy usage.
- Identify peak usage periods and low usage baseline periods deterministically.

## 6. Deterministic Anomaly Detection
- Apply transparent statistical methods (Z-score, Interquartile Range [IQR], or configurable threshold).
- Identify unusual energy spikes or abnormal consumption entries.
- Output anomaly scores, detection thresholds, and detailed human-readable explanations of why records were flagged.

## 7. Financial Cost Estimation
- Calculate estimated energy cost using the deterministic formula: `cost = total_kwh × tariff_per_kwh`.
- Validate tariff parameter presence and return structured error (`INVALID_TARIFF`) if tariff inputs are missing or invalid.

## 8. Energy-Saving Recommendations
- Generate automated analytical efficiency suggestions based on actual dataset statistics.
- Highlight high-consumption categories, peak usage window shifts, and detected anomalies.
- Append explicit disclaimers clarifying that suggestions are analytical only and not professional engineering advice.

## 9. Comprehensive Report Synthesis
- Assemble comprehensive, JSON-compatible energy reports aggregating summary statistics, appliance breakdowns, temporal patterns, anomalies, cost estimates, and recommendations.

## 10. Portability & Integrity Maintenance
- Maintain complete framework-independent portability.
- Ensure 100% deterministic local execution without hidden external API dependencies or opaque black-box AI reasoning.
