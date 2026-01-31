# Ethiopia-fi-forecast
📌 Project Overview

This project builds a data-driven system to analyze and forecast financial inclusion in Ethiopia, focusing on two Global Findex dimensions:

Access – Account Ownership Rate

Usage – Digital Payment Adoption Rate

The work is structured into sequential tasks, where each task builds directly on the outputs of the previous one.
This README documents Task 1 (Data Exploration & Enrichment) and Task 2 (Exploratory Data Analysis).

🧩 Task 1: Data Exploration and Enrichment
🎯 Objective

To understand the starter dataset, validate its structure, and enrich it with additional data that improves the ability to forecast financial inclusion outcomes in Ethiopia.

Task 1 establishes a clean, reliable, and auditable data foundation for all downstream modeling and forecasting.

📂 Data Sources
Starter Dataset

Located in:

data/raw/


Files used:

ethiopia_fi_unified_data.csv

reference_codes.csv

The unified dataset follows a single schema where the meaning of each row depends on the record_type field.

🧱 Dataset Schema Understanding
Record Types
record_type	Description
observation	Measured values from surveys, reports, and operators
event	Policies, product launches, infrastructure milestones
target	Official policy goals (e.g., NFIS targets)
Key Design Principle

Events are NOT assigned pillars (Access / Usage)

Event effects are modeled separately using impact_links

This avoids bias and double counting

🔗 Impact Links

Stored as a separate logical dataset

Connect events → indicators

Include:

Impact direction

Magnitude

Lag (months)

Evidence basis

This separation allows flexible modeling in later tasks.

🔍 Exploratory Checks Performed

Record counts by:

record_type

pillar

source_type

confidence

Temporal coverage of observations

Unique indicators and data availability

Event inventory and event dates

Review of existing impact relationships

➕ Data Enrichment

To improve forecasting quality, the dataset was enriched with:

Additional Observations

Examples:

Smartphone penetration

Mobile broadband coverage

Agent density

Gender-disaggregated indicators (where available)

These variables act as leading indicators and enablers for digital financial inclusion.

Additional Events

Examples:

Interoperable payment infrastructure rollout

Safaricom Ethiopia market entry

Digital ID expansion milestones

All new events:

Have a category

Leave pillar empty (by design)

Additional Impact Links

New modeled relationships were added to capture:

Infrastructure → Usage effects

Policy → Access effects

Product launches → Usage acceleration (lagged)

🧪 Validation & Robustness

Basic validations were applied to ensure data integrity:

Valid record_type values only

Events have no pillar assigned

Observations contain numeric values

Required fields are present

No silent failures (errors are explicit)

📝 Documentation & Audit Trail

All additions are documented in:

reports/data_enrichment_log.md


For each new record, the log includes:

Source URL

Original quoted text

Confidence assessment

Collection date

Rationale for inclusion

This ensures transparency and reproducibility.

📦 Outputs of Task 1

Enriched dataset saved to:

data/processed/ethiopia_fi_unified_data_enriched.csv


Reusable data loading and validation logic

Fully reproducible notebook execution

Clean handoff to Task 2 (EDA)

📈 Task 2: Exploratory Data Analysis (EDA)
🎯 Objective

To analyze the enriched dataset and understand patterns, drivers, gaps, and anomalies in Ethiopia’s financial inclusion trajectory.

Task 2 transforms data into insight, preparing the ground for event impact modeling (Task 3).

🔎 Dataset Overview Analysis

The dataset was summarized by:

record_type

pillar

source_type

confidence

Key Observations

Observations dominate the dataset

Events are fewer but strategically important

Medium-confidence data is common → uncertainty acknowledged

🕒 Temporal Coverage Analysis

Visualized which indicators have data across which years

Identified sparse coverage for:

Global Findex indicators

Gender and rural/urban splits

📌 Implication:
Pure time-series models are limited → hybrid and event-augmented approaches are needed.

🔐 Access (Account Ownership) Analysis
Findings

Strong growth from 2011 to 2021

Sharp slowdown from 2021 to 2024 (+3 percentage points)

Growth Rate Analysis

Calculated growth between survey years

Confirmed structural deceleration post-2021

Interpretation

Despite massive mobile money expansion:

Many accounts are dormant or secondary

Mobile money often adds convenience, not new formal access

Findex definition limits what counts as “access”

💳 Usage (Digital Payments) Analysis
Patterns Observed

Rapid growth in registered mobile money accounts

Slower growth in actual digital payment usage

Key Insight

A clear registered vs. active usage gap exists:

Registration ≠ meaningful usage

Usage depends on infrastructure, trust, and use cases

🏗 Infrastructure & Enablers

Analyzed indicators such as:

Smartphone penetration

Mobile broadband coverage

Agent density

ATM density

Findings

Infrastructure indicators correlate more strongly with Usage than Access

Many act as leading indicators with lagged effects

📅 Event Timeline Analysis

Events were plotted on a timeline and visually compared against indicator trends.

Key observations:

Telebirr launch boosted mobile money usage, not account ownership

Safaricom entry showed delayed effects

M-Pesa entry increased competition, not immediate inclusion

🔗 Correlation Analysis

Correlation analysis revealed:

Usage indicators are more tightly coupled with infrastructure

Access indicators weaken in correlation after 2021

This reinforces the need for event-based modeling.

🧠 Key Insights (Summary)

Financial inclusion growth in Ethiopia is slowing structurally, not temporarily.

Mobile money expansion affects usage more than access.

Infrastructure is a stronger predictor of usage than policy alone.

Findex-defined access may understate real digital participation.

Data sparsity limits pure statistical forecasting.

⚠️ Data Quality & Limitations

Sparse survey years (Global Findex every ~3 years)

Mixed confidence levels across sources

Operator data not always comparable to survey data

Limited disaggregation (gender, rural/urban)