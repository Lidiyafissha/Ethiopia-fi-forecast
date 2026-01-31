import pandas as pd
import matplotlib.pyplot as plt


def summarize_dataset(df):
    return {
        "by_record_type": df["record_type"].value_counts(),
        "by_pillar": df["pillar"].value_counts(dropna=False),
        "by_source_type": df["source_type"].value_counts(dropna=False),
        "by_confidence": df["confidence"].value_counts(dropna=False),
    }


def temporal_coverage(df):
    coverage = (
        df.dropna(subset=["indicator_code", "observation_date"])
          .assign(year=lambda x: x["observation_date"].dt.year)
          .groupby(["indicator_code", "year"])
          .size()
          .reset_index(name="count")
    )
    return coverage


def plot_indicator(df, indicator_code, title):
    sub = df[df["indicator_code"] == indicator_code].sort_values("observation_date")
    plt.figure(figsize=(8, 4))
    plt.plot(sub["observation_date"], sub["value_numeric"], marker="o")
    plt.title(title)
    plt.ylabel("% of adults")
    plt.xlabel("Year")
    plt.grid(True)
    plt.show()


def growth_rates(df, indicator_code):
    sub = df[df["indicator_code"] == indicator_code].sort_values("observation_date")
    sub["growth_pp"] = sub["value_numeric"].diff()
    return sub[["observation_date", "value_numeric", "growth_pp"]]
