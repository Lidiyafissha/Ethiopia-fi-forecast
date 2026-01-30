import uuid
import pandas as pd


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def add_observation(df, record: dict) -> pd.DataFrame:
    record["id"] = generate_id("obs")
    record["record_type"] = "observation"
    return pd.concat([df, pd.DataFrame([record])], ignore_index=True)


def add_event(df, record: dict) -> pd.DataFrame:
    record["id"] = generate_id("evt")
    record["record_type"] = "event"
    record["pillar"] = None
    return pd.concat([df, pd.DataFrame([record])], ignore_index=True)


def add_impact_link(df, record: dict) -> pd.DataFrame:
    record["id"] = generate_id("imp")
    return pd.concat([df, pd.DataFrame([record])], ignore_index=True)
