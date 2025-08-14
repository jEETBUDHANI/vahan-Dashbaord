import pandas as pd
from pathlib import Path

DATE_COL = "date"
CAT_COL = "category"
MFG_COL = "manufacturer"
VAL_COL = "registrations"

def load_data(data_path_or_df):
    """
    Accepts a CSV path or a pandas DataFrame.
    Ensures correct dtypes and standard column names.
    Expected columns: date, category, manufacturer, registrations
    """
    if isinstance(data_path_or_df, (str, Path)):
        df = pd.read_csv(data_path_or_df)
    else:
        df = data_path_or_df.copy()
    # Standardize column names (case-insensitive)
    rename_map = {c.lower():c for c in df.columns}
    # Normalize: force our expected names
    normalized = {}
    for c in df.columns:
        cl = c.strip().lower()
        if cl in ["date","month","dt"]:
            normalized[c] = DATE_COL
        elif cl in ["category","vehicle_category","vehicle_class","type","veh_type"]:
            normalized[c] = CAT_COL
        elif cl in ["manufacturer","oem","make"]:
            normalized[c] = MFG_COL
        elif cl in ["registrations","count","total","value","qty","number"]:
            normalized[c] = VAL_COL

    df = df.rename(columns=normalized)
    missing = {DATE_COL, CAT_COL, MFG_COL, VAL_COL} - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found columns: {list(df.columns)}")

    # Parse date
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    if df[DATE_COL].isna().any():
        raise ValueError("Some 'date' values could not be parsed. Ensure YYYY-MM-DD or similar format.")

    # Clean
    df[CAT_COL] = df[CAT_COL].astype(str).str.strip().str.upper().replace({"FOUR WHEELER":"4W","TWO WHEELER":"2W","THREE WHEELER":"3W"})
    df[MFG_COL] = df[MFG_COL].astype(str).str.strip()
    df[VAL_COL] = pd.to_numeric(df[VAL_COL], errors="coerce").fillna(0).astype(int)

    return df.sort_values(DATE_COL).reset_index(drop=True)

def add_time_parts(df):
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df
