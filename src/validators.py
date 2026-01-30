def validate_record_types(df):
    allowed = {"observation", "event", "target"}
    invalid = set(df["record_type"].dropna()) - allowed
    if invalid:
        raise ValueError(f"Invalid record_type values: {invalid}")


def validate_events_have_no_pillar(df):
    events = df[df["record_type"] == "event"]
    if events["pillar"].notna().any():
        raise ValueError("Events must not have pillar values")


def validate_observations_have_values(df):
    obs = df[df["record_type"] == "observation"]
    if obs["value_numeric"].isna().any():
        raise ValueError("Some observations have missing numeric values")


def run_all_validations(df):
    validate_record_types(df)
    validate_events_have_no_pillar(df)
    validate_observations_have_values(df)
