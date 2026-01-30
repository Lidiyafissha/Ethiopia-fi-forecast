import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = [
    "record_id", "record_type", "pillar", "indicator", "indicator_code",
    "value_numeric", "observation_date", "source_name",
    "source_url", "confidence"
]


def load_csv_safe(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to read {path.name}: {e}")

    return df


def load_unified_data(base_path: Path) -> pd.DataFrame:
    df = load_csv_safe(base_path / "ethiopia_fi_unified_data.csv")

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["observation_date"] = pd.to_datetime(
        df["observation_date"], errors="coerce"
    )

    df["value_numeric"] = pd.to_numeric(
        df["value_numeric"], errors="coerce"
    )

    return df


def load_reference_codes(base_path: Path) -> pd.DataFrame:
    return load_csv_safe(base_path / "reference_codes.csv")


def load_impact_links(base_path: Path) -> pd.DataFrame:
    path = base_path / "impact_links.csv"

    if path.exists():
        df = load_csv_safe(path)
        if "parent_id" not in df.columns:
            raise ValueError("impact_links must contain parent_id")
        return df

    # Build impact links heuristically from the unified dataset when explicit file is missing.
    unified = load_unified_data(base_path)

    # Ensure key columns exist
    for col in ("record_id", "record_type", "observation_date"):
        if col not in unified.columns:
            raise ValueError(f"unified data missing required column: {col}")

    events = unified[unified["record_type"] == "event"].copy()
    observations = unified[unified["record_type"] == "observation"].copy()

    links = []

    # normalize text helper
    def _text(val):
        return str(val).lower() if pd.notna(val) else ""

    for _, ev in events.iterrows():
        try:
            ev_date = pd.to_datetime(ev.get("observation_date"), errors="coerce")
        except Exception:
            ev_date = pd.NaT

        # candidate observations after the event date (or all if event date missing)
        if pd.notna(ev_date):
            cand = observations[pd.to_datetime(observations["observation_date"], errors="coerce") >= ev_date]
        else:
            cand = observations

        # score candidates by simple heuristics: shared source_url/name or mention of indicator in notes/text
        scored = []
        ev_src = _text(ev.get("source_url") or ev.get("source_name"))
        ev_notes = _text(ev.get("notes")) + " " + _text(ev.get("original_text"))

        for _, ob in cand.iterrows():
            score = 0
            ob_src = _text(ob.get("source_url") or ob.get("source_name"))
            ob_notes = _text(ob.get("notes")) + " " + _text(ob.get("original_text"))

            if ev_src and ob_src and ev_src == ob_src:
                score += 10

            # indicator name matching
            if pd.notna(ev.get("indicator")) and pd.notna(ob.get("indicator")):
                if _text(ev.get("indicator")) == _text(ob.get("indicator")):
                    score += 8

            # text overlap
            if ev.get("indicator") and ev.get("indicator").lower() in ob_notes:
                score += 6
            if ob.get("indicator") and ob.get("indicator").lower() in ev_notes:
                score += 6

            # temporal proximity bonus (smaller lag => higher score)
            try:
                ob_date = pd.to_datetime(ob.get("observation_date"), errors="coerce")
                if pd.notna(ev_date) and pd.notna(ob_date):
                    days = (ob_date - ev_date).days
                    if days >= 0 and days <= 365 * 2:
                        score += max(0, 5 - int(days / 365))
            except Exception:
                pass

            if score > 0:
                scored.append((score, ev["record_id"], ob["record_id"], ev_date, ob_date if 'ob_date' in locals() else None, ev_src == ob_src))

        # sort scored candidates and take top matches (limit to 5)
        scored.sort(reverse=True, key=lambda x: x[0])
        for s in scored[:5]:
            score, parent_id, child_id, evd, obd, same_source = s
            lag_months = None
            if pd.notna(evd) and pd.notna(obd):
                lag_months = int(((obd - evd).days) / 30)

            links.append({
                "parent_id": parent_id,
                "child_id": child_id,
                "relationship_type": "direct" if same_source else "indirect",
                "impact_direction": None,
                "impact_magnitude": None,
                "evidence_basis": "empirical" if same_source else "expert",
                "lag_months": lag_months,
                "score": score,
            })

    if not links:
        # return empty DataFrame with expected columns
        return pd.DataFrame(columns=["parent_id", "child_id", "relationship_type", "impact_direction", "impact_magnitude", "evidence_basis", "lag_months", "score"])

    return pd.DataFrame(links)
