import streamlit as st
import pandas as pd
from src.data_utils import load_data, add_time_parts
from src.metrics import agg_by, trend_and_growth
from src.ui_components import time_series_chart, growth_bar

st.set_page_config(page_title="Vahan Investor Dashboard", layout="wide")

st.title("Vahan Investor Dashboard")
st.caption("Investor-focused insights on vehicle registrations (YoY & QoQ). Upload Vahan exports or use the sample data.")

# Sidebar: data source
with st.sidebar:
    st.header("Data")
    src_choice = st.radio("Choose data source", ["Use sample dataset", "Upload CSV"])
    if src_choice == "Upload CSV":
        up = st.file_uploader("Upload CSV with columns: date, category, manufacturer, registrations", type=["csv"])
        if up:
            df = load_data(pd.read_csv(up))
        else:
            st.stop()
    else:
        df = load_data("data/sample_registrations.csv")
    df = add_time_parts(df)

    st.markdown("---")
    st.header("Filters")
    years = sorted(df["year"].unique())
    year_range = st.slider("Year range", min_value=int(min(years)), max_value=int(max(years)),
                           value=(int(min(years)), int(max(years))))
    cats = sorted(df["category"].unique())
    sel_cats = st.multiselect("Vehicle categories", cats, default=cats)
    mfgs = sorted(df["manufacturer"].unique())
    default_mfgs = mfgs if len(mfgs) <= 10 else mfgs[:10]
    sel_mfgs = st.multiselect("Manufacturers", mfgs, default=default_mfgs)

    st.markdown("---")
    st.header("View Options")
    view = st.selectbox("View", ["By Category", "By Manufacturer"])

# Apply filters
mask = (df["year"].between(year_range[0], year_range[1])) & df["category"].isin(sel_cats) & df["manufacturer"].isin(sel_mfgs)
df_f = df[mask].copy()

# KPI cards
def kpi_block(label, value, delta=None):
    st.metric(label, f"{value:,.0f}", delta=None if delta is None else f"{delta:+.1f}%")

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
monthly_total = df_f.set_index("date")["registrations"].resample("M").sum()
yoy = monthly_total.pct_change(12).iloc[-1] * 100 if len(monthly_total) >= 13 else None
qoq = monthly_total.resample("Q").sum().pct_change(1).iloc[-1] * 100 if len(monthly_total)>=4 else None
with col1: kpi_block("Total Registrations (selected)", monthly_total.sum())
with col2: kpi_block("Latest YoY %", 0 if pd.isna(yoy) else yoy)
with col3: kpi_block("Latest QoQ %", 0 if pd.isna(qoq) else qoq)

st.markdown("---")

if view == "By Category":
    # Trend by category
    agg = agg_by(df_f, "date", ["category"], "registrations", freq="M", how="sum")
    trend = trend_and_growth(agg, "date", ["category"], "registrations")
    st.altair_chart(time_series_chart(trend, x="date", y="registrations", color="category",
                                      title="Monthly Registrations by Category"), use_container_width=True)
    st.altair_chart(growth_bar(trend.dropna(subset=["yoy_%"]), x="date", y="yoy_%", color="category",
                               title="YoY Growth % by Category"), use_container_width=True)
    # QoQ bar
    qtr = (trend.groupby(["category","quarter"])["registrations"].sum()
                .groupby(level=0).pct_change().reset_index(name="qoq_%"))
    qtr["date"] = pd.PeriodIndex(qtr["quarter"], freq="Q").to_timestamp(how="end")
    st.altair_chart(growth_bar(qtr.dropna(subset=["qoq_%"]), x="date", y="qoq_%", color="category",
                               title="QoQ Growth % by Category"), use_container_width=True)

else:
    agg = agg_by(df_f, "date", ["manufacturer"], "registrations", freq="M", how="sum")
    trend = trend_and_growth(agg, "date", ["manufacturer"], "registrations")
    st.altair_chart(time_series_chart(trend, x="date", y="registrations", color="manufacturer",
                                      title="Monthly Registrations by Manufacturer"), use_container_width=True)
    st.altair_chart(growth_bar(trend.dropna(subset=["yoy_%"]), x="date", y="yoy_%", color="manufacturer",
                               title="YoY Growth % by Manufacturer"), use_container_width=True)
    qtr = (trend.groupby(["manufacturer","quarter"])["registrations"].sum()
                .groupby(level=0).pct_change().reset_index(name="qoq_%"))
    qtr["date"] = pd.PeriodIndex(qtr["quarter"], freq="Q").to_timestamp(how="end")
    st.altair_chart(growth_bar(qtr.dropna(subset=["qoq_%"]), x="date", y="qoq_%", color="manufacturer",
                               title="QoQ Growth % by Manufacturer"), use_container_width=True)

# Investor insights (auto-generated bullets)
st.markdown("---")
st.subheader("Auto Insights (Investor Lens)")
# Identify top growing manufacturers YoY (last 3 months avg vs same period prev year)
last3 = df_f.set_index("date").last("3M").groupby("manufacturer")["registrations"].sum()
prev3 = df_f.set_index("date").shift(12).last("3M").groupby("manufacturer")["registrations"].sum()
growth = ((last3 - prev3) / prev3 * 100).sort_values(ascending=False)
st.write("- Top 5 manufacturers by YoY growth (last 3 months vs LY):")
for m, g in growth.head(5).items():
    st.write(f"  - **{m}**: {g:.1f}%")

# Category mix shift
mix_now = df_f.set_index("date").last("3M").groupby("category")["registrations"].sum()
mix_prev = df_f.set_index("date").shift(12).last("3M").groupby("category")["registrations"].sum()
mix_change = ((mix_now / mix_now.sum()) - (mix_prev / (mix_prev.sum() if mix_prev.sum()>0 else 1))) * 100
st.write("- Category mix shift (share change vs last year, last 3 months):")
for c, v in mix_change.sort_values(ascending=False).items():
    st.write(f"  - **{c}**: {v:+.1f} pp")

st.info("Tip: Replace the sample CSV with Vahan exports. Use the sidebar to filter by years, category, and manufacturers.")
