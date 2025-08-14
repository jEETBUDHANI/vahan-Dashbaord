import altair as alt
import pandas as pd

def time_series_chart(df, x="date", y="registrations", color=None, tooltip=None, title=None):
    if tooltip is None:
        tooltip = [x, y]
        if color: tooltip.append(color)
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(x, title="Date"),
        y=alt.Y(y, title="Registrations"),
        color=color,
        tooltip=tooltip,
    )
    if title:
        chart = chart.properties(title=title)
    return chart.interactive()

def growth_bar(df, x="date", y="yoy_%", color=None, title=None):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x, title="Date"),
        y=alt.Y(y, title="Growth %"),
        color=color,
        tooltip=[x, y] + ([color] if color else []),
    )
    if title:
        chart = chart.properties(title=title)
    return chart.interactive()
