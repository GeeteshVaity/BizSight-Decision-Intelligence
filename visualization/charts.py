import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def revenue_trend_chart(df: pd.DataFrame):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    grouped = df.groupby("month", as_index=False)["revenue"].sum()

    fig = px.line(
        grouped,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
    )

    fig.update_layout(
        hovermode="x unified",
        template="plotly_white"
    )

    return fig



def profit_by_product_chart(df: pd.DataFrame):
    grouped = df.groupby("product_name", as_index=False)["profit"].sum()

    fig = px.bar(
        grouped,
        x="product_name",
        y="profit",
        title="Profit by Product",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Product",
        yaxis_title="Profit",
        template="plotly_white"
    )

    return fig



def revenue_contribution_pie(df: pd.DataFrame):
    grouped = df.groupby("product_name", as_index=False)["revenue"].sum()

    fig = px.pie(
        grouped,
        values="revenue",
        names="product_name",
        title="Revenue Contribution by Product",
        hole=0.4  # donut chart = modern 😎
    )

    fig.update_traces(textposition="inside", textinfo="percent")

    fig.update_layout(template="plotly_white")

    return fig


