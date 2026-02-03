import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    layout="wide"
)

st.title("📊 Ethiopia Financial Inclusion Dashboard")
st.caption("Access • Usage • Events • Forecasts")


# -------------------------------
# Data Loading (Robust)
# -------------------------------

# Project root (two levels up from dashboard/)
BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "ethiopia_fi_unified_data.csv"
FORECAST_PATH = BASE_DIR / "data" / "processed" / "forecasts.csv"

def load_csv(path: Path, name: str):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"❌ {name} not found at: {path}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading {name}: {e}")
        return None

df_raw = load_csv(RAW_DATA_PATH, "Raw financial inclusion data")
df_forecast = load_csv(FORECAST_PATH, "Forecast data")

if df_raw is None or df_forecast is None:
    st.stop()


st.success("✅ Data loaded successfully")
st.write("Raw data shape:", df_raw.shape)
st.write("Forecast data shape:", df_forecast.shape)

st.write(
    df_raw["indicator_code"]
    .value_counts()
)


# @st.cache_data
# def load_data():
#     data = pd.read_csv(BASE_DIR / "data" / "raw" / "ethiopia_fi_unified_data.csv")
#     forecasts_path = BASE_DIR / "data" / "processed" / "forecasts.csv"
#     if forecasts_path.exists():
#         forecasts = pd.read_csv(forecasts_path)
#     else:
#         forecasts = pd.DataFrame()
#     return data, forecasts

# try:
#     df, forecast_df = load_data()
# except Exception as e:
#     st.error(f"Error loading data: {e}")
#     st.stop()

# -------------------------------
# Sidebar Navigation
# -------------------------------
page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Trends",
        "Forecasts",
        "Inclusion Projections"
    ]
)

# -------------------------------
# Helper Filters
# -------------------------------
access_code = "ACC_OWNERSHIP"
usage_code = "USG_DIGITAL_PAYMENT"

# ===============================
# OVERVIEW PAGE
# ===============================
if page == "Overview":
    st.header("📌 Overview")

    if "observation_date" in df_raw.columns:
        df_raw["observation_date"] = pd.to_datetime(
            df_raw["observation_date"], errors="coerce"
        )
        df_raw["year"] = df_raw["observation_date"].dt.year
    else:
        st.error("❌ observation_date column missing")
        st.stop()

    #latest_year = df_raw["year"].max()
    latest_year = df_raw["year"].max()

    # Extract access_latest safely
    access_filtered = df_raw[df_raw["indicator_code"] == access_code].sort_values("year")
    if access_filtered.empty:
        st.error("❌ No account ownership data available")
        st.stop()
    access_latest = access_filtered.iloc[-1]["value_numeric"]


    usage_df = df_raw[
        (df_raw["record_type"] == "observation") &
        (df_raw["indicator_code"] == "USG_DIGITAL_PAYMENT") &
        (df_raw["value_numeric"].notna())
    ].sort_values("observation_date")

    if usage_df.empty:
        st.warning("⚠️ No digital payment usage data available.")
        usage_latest_value = None
    else:
        usage_latest_value = usage_df.iloc[-1]["value_numeric"]

    if usage_latest_value is not None:
        st.metric(
            label="Digital Payment Usage (%)",
            value=f"{usage_latest_value:.1f}%"
        )
    else:
        st.metric(
            label="Digital Payment Usage (%)",
            value="N/A"
        )


    # usage_latest = df_raw[
    #     df_raw["indicator_code"] == usage_code
    # ].sort_values("year").iloc[-1]["value_numeric"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Account Ownership (%)", f"{access_latest:.1f}")
    if usage_latest_value is not None:
        col2.metric("Digital Payment Usage (%)", f"{usage_latest_value:.1f}")
    else:
        col2.metric("Digital Payment Usage (%)", "N/A")
    col3.metric("Latest Data Year", int(latest_year))

    st.markdown("---")

    st.subheader("📈 Growth Highlights")

    # Calculate growth safely
    access_growth_df = df_raw[df_raw["indicator_code"] == access_code].sort_values("year")
    if "value_numeric" in access_growth_df.columns and not access_growth_df.empty:
        growth_access = access_growth_df["value_numeric"].diff().mean()
    else:
        growth_access = 0

    usage_growth_df = df_raw[df_raw["indicator_code"] == usage_code].sort_values("year")
    if "value_numeric" in usage_growth_df.columns and not usage_growth_df.empty:
        growth_usage = usage_growth_df["value_numeric"].diff().mean()
    else:
        growth_usage = 0

    # Handle NaN values
    if pd.isna(growth_access):
        growth_access = 0
    if pd.isna(growth_usage):
        growth_usage = 0

    st.write(f"- **Average Access Growth:** {growth_access:.2f} pp per period")
    st.write(f"- **Average Usage Growth:** {growth_usage:.2f} pp per period")

# ===============================
# TRENDS PAGE
# ===============================
elif page == "Trends":
    st.header("📈 Historical Trends")

    indicator = st.selectbox(
        "Select Indicator",
        {
            "Account Ownership": access_code,
            "Digital Payment Usage": usage_code
        }
    )

    filtered = df_raw[df_raw["indicator_code"] == indicator]

    if filtered.empty:
        st.warning(f"No data available for {indicator}")
    else:
        fig = px.line(
            filtered,
            x="year",
            y="value_numeric",
            markers=True,
            title="Indicator Trend Over Time",
            labels={
                "value_numeric": "Percentage (%)",
                "year": "Year"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

# ===============================
# FORECASTS PAGE
# ===============================
elif page == "Forecasts":
    st.header("🔮 Forecasts (2025–2027)")

    scenario = st.selectbox(
        "Select Scenario",
        ["base", "optimistic", "pessimistic"]
    )

    indicator = st.selectbox(
        "Select Indicator",
        {
            "Account Ownership": "access",
            "Digital Payment Usage": "usage"
        }
    )

    forecast_filtered = df_forecast[
        (df_forecast["scenario"] == scenario) &
        (df_forecast["indicator"] == indicator)
    ]

    if forecast_filtered.empty:
        st.warning("No forecast data available for the selected combination.")
    else:
        fig = px.line(
            forecast_filtered,
            x="year",
            y="forecast",
            title="Forecast with Scenario",
            markers=True
        )

        fig.add_scatter(
            x=forecast_filtered["year"],
            y=forecast_filtered["lower_ci"],
            mode="lines",
            name="Lower CI",
            line=dict(dash="dash")
        )

        fig.add_scatter(
            x=forecast_filtered["year"],
            y=forecast_filtered["upper_ci"],
            mode="lines",
            name="Upper CI",
            line=dict(dash="dash")
        )

        st.plotly_chart(fig, use_container_width=True)

# ===============================
# INCLUSION PROJECTIONS PAGE
# ===============================
elif page == "Inclusion Projections":
    st.header("🎯 Inclusion Projections")

    target = 60

    access_forecast = df_forecast[
        (df_forecast["indicator"] == "access") &
        (df_forecast["scenario"] == "base")
    ]

    if access_forecast.empty:
        st.warning("No forecast data available.")
    else:
        fig = px.line(
            access_forecast,
            x="year",
            y="forecast",
            markers=True,
            title="Progress Toward 60% Financial Inclusion Target"
        )

        fig.add_hline(
            y=target,
            line_dash="dash",
            annotation_text="60% Target"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Interpretation:**
        - Current trends suggest gradual progress
        - Achieving 60% requires accelerated usage, not just account creation
        """)
