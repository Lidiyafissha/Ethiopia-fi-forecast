#Ethiopia Financial Inclusion Forecasting
Overview

This project tracks and forecasts Ethiopia’s financial inclusion progress, focusing on two core Global Findex indicators:

Account Ownership (Access) – Share of adults with a financial account or mobile money.

Digital Payment Usage (Usage) – Share of adults making or receiving digital payments.

The system provides insights into historical trends, event-driven impacts, and projections for 2025–2027, helping stakeholders make informed decisions on policies, product launches, and infrastructure development.

Project Structure
ethiopia-fi-forecast/
├── data/
│   ├── raw/                  # Original datasets
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/            # Cleaned and enriched datasets
│       └── forecasts.csv
├── notebooks/                # EDA, impact modeling, forecasting
├── src/                      # Reusable scripts (data loading, processing)
├── dashboard/
│   └── app.py                # Streamlit dashboard
├── reports/                  # Figures and summaries
├── tests/                    # Unit tests
├── requirements.txt
└── README.md

Tasks
Task 1 – Data Exploration & Enrichment

Objective: Understand the starter dataset and enrich it with additional observations, events, and impact links.

Actions Taken:

Explored ethiopia_fi_unified_data.csv and impact_links.

Validated records by record_type, pillar, indicator_code, confidence.

Enriched dataset with additional infrastructure, policy, and market events.

Logged sources, confidence levels, and collection notes in data_enrichment_log.md.

Outcome:
A clean, enriched dataset ready for analysis and modeling.

Task 2 – Exploratory Data Analysis (EDA)

Objective: Analyze patterns, gaps, and key factors influencing financial inclusion.

Actions Taken:

Summarized data by record_type, pillar, and source_type.

Visualized temporal coverage for all indicators.

Analyzed trends in account ownership and digital payment usage (2011–2024).

Explored gender and urban/rural disparities.

Investigated 2021–2024 slowdown in account ownership growth.

Mapped events on indicator trends to identify potential influences.

Assessed data quality and gaps.

Outcome:
EDA notebook highlighting trends, correlations, and five key insights into Ethiopia’s financial inclusion dynamics.

Task 3 – Event Impact Modeling

Objective: Quantify how events (policies, product launches, infrastructure) affect inclusion indicators.

Actions Taken:

Merged events with impact links to create an event-indicator matrix.

Calculated directional and magnitude impacts over time.

Validated model estimates against historical outcomes (e.g., Telebirr, M-Pesa launches).

Documented assumptions, limitations, and uncertainties.

Outcome:
A robust model that translates events into expected changes in access and usage metrics.

Task 4 – Forecasting Access and Usage

Objective: Forecast 2025–2027 values for account ownership and digital payment usage.

Approach:

Trend regression with event-augmented adjustments.

Scenario analysis: Optimistic, Base, Pessimistic.

Quantified uncertainty using confidence intervals.

Results:

Consolidated forecasts in forecasts.csv.

Account ownership expected to rise gradually; digital payment usage projected to grow faster.

Event-driven effects (e.g., new infrastructure, policy changes) incorporated.

Outcome:
Structured dataset for dashboard integration and downstream visualization.

Task 5 – Dashboard Development

Objective: Enable stakeholders to interactively explore historical trends, event impacts, and forecasts.

Implementation:

Streamlit-based dashboard (dashboard/app.py) with four main sections:

Overview – Key metrics, P2P/ATM crossover ratio, growth highlights.

Trends – Time-series plots, date range selector, channel comparisons.

Forecasts – Scenario-based projections with confidence intervals.

Inclusion Projections – Progress toward 60% target, scenario selector.

Interactive visualizations with download functionality.

Clear labels, guidance, and run instructions included.

Outcome:
A fully interactive tool for exploring Ethiopia’s financial inclusion landscape and scenario-based forecasts.

Installation & Usage
# Clone the repository
git clone <repo_url>
cd ethiopia-fi-forecast

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/app.py

Key Insights

Account ownership growth slowed 2021–2024 despite large mobile money uptake.

Digital payment usage is rising faster than account ownership.

Event timing (product launches, policies) strongly influences trends.

Gender and urban/rural gaps persist.

Infrastructure expansion (mobile coverage, ATMs) is a key enabler.