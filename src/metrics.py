import pandas as pd

def yoy_growth(series: pd.Series):
    """Compute Year-over-Year growth % for a monthly series indexed by date."""
    s = series.sort_index()
    comp = s.pct_change(12) * 100
    return comp

def qoq_growth(series: pd.Series):
    """Compute Quarter-over-Quarter growth % for a monthly series indexed by date."""
    s = series.sort_index().resample("Q").sum()
    comp = s.pct_change(1) * 100
    return comp

def agg_by(df, date_col, group_cols, value_col, freq="M", how="sum"):
    """Aggregate time series by frequency and group dimensions."""
    g = df.set_index(date_col)
    if how == "sum":
        out = g.groupby(group_cols).resample(freq)[value_col].sum().reset_index()
    elif how == "mean":
        out = g.groupby(group_cols).resample(freq)[value_col].mean().reset_index()
    else:
        raise ValueError("Unsupported aggregation")
    return out

def trend_and_growth(df, date_col, group_cols, value_col):
    """Return original monthly trend plus YoY & QoQ growth per group."""
    res = []

    for keys, g in df.groupby(group_cols):
        ts = g.set_index(date_col)[value_col].resample("M").sum()

        out = pd.DataFrame({
            date_col: ts.index,
            value_col: ts.values,
            "yoy_%": yoy_growth(ts).reindex(ts.index).values,
        })

        # QoQ growth
        qoq = qoq_growth(ts)
        qoq.index = qoq.index.to_period("Q").astype(str)  # make index strings

        # Ensure date column is datetime before to_period
        out[date_col] = pd.to_datetime(out[date_col])
        out["quarter"] = pd.to_datetime(out[date_col]).dt.to_period("Q").astype(str)

        # Merge QoQ into out
        out = out.merge(
            qoq.rename("qoq_%"),
            left_on="quarter",
            right_index=True,
            how="left"
        )

        out["qoq_%"] = out["qoq_%"].fillna(0)  # Fill NaN with 0 for QoQ growth

        # Attach group columns
        if isinstance(keys, tuple):
            for k, name in zip(keys, group_cols):
                out[name] = k
        else:
            out[group_cols[0]] = keys

        res.append(out)

    return pd.concat(res, ignore_index=True)
