from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def revenue_trend(df: pd.DataFrame) -> go.Figure:
    fig = px.line(df, x="order_date", y="daily_revenue", labels={"daily_revenue": "Daily revenue", "order_date": "Date"})
    fig.add_scatter(x=df["order_date"], y=df["rolling_7d"], mode="lines", name="7-day average", line={"color": "#0A4C6A", "width": 3})
    fig.update_layout(title="Revenue trend")
    return fig


def monthly_revenue(df: pd.DataFrame) -> go.Figure:
    fig = px.bar(df, x="order_date", y="line_total", labels={"line_total": "Revenue", "order_date": "Month"})
    fig.update_layout(title="Monthly revenue")
    return fig


def ranked_bar(df: pd.DataFrame, x: str, y: str, title: str) -> go.Figure:
    fig = px.bar(df.sort_values(y), x=y, y=x, orientation="h", labels={x: "", y: "Revenue"})
    fig.update_layout(title=title, height=420)
    return fig


def cohort_heatmap(df: pd.DataFrame) -> go.Figure:
    matrix = df.copy()
    matrix.index = matrix.index.astype(str)
    fig = px.imshow(matrix, text_auto=".0%", aspect="auto", color_continuous_scale="Blues", labels={"x": "Month", "y": "Cohort", "color": "Retention"})
    fig.update_layout(title="Monthly cohort retention")
    return fig


def cohort_size_bar(df: pd.DataFrame) -> go.Figure:
    sizes = df.iloc[:, 0].rename("cohort_size").reset_index()
    sizes["cohort"] = sizes["cohort"].astype(str)
    fig = px.bar(sizes, x="cohort", y="cohort_size", labels={"cohort": "Cohort", "cohort_size": "Initial customers"})
    fig.update_layout(title="Cohort size", height=320)
    return fig


def rfm_segments(df: pd.DataFrame) -> go.Figure:
    counts = df["segment"].astype(str).value_counts().reset_index()
    counts.columns = ["segment", "customers"]
    fig = px.bar(counts, x="segment", y="customers", labels={"segment": "Segment", "customers": "Customers"})
    fig.update_layout(title="RFM customer segments")
    return fig


def abc_mix(df: pd.DataFrame) -> go.Figure:
    counts = df["abc_class"].astype(str).value_counts().sort_index().reset_index()
    counts.columns = ["abc_class", "products"]
    fig = px.pie(counts, names="abc_class", values="products", hole=0.52)
    fig.update_layout(title="ABC inventory mix")
    return fig
