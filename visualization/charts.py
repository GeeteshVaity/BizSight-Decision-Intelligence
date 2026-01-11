import matplotlib.pyplot as plt
import pandas as pd


def revenue_trend_chart(df: pd.DataFrame):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    grouped = df.groupby(df["Date"].dt.to_period("M"))["Revenue"].sum()
    grouped.index = grouped.index.to_timestamp()

    plt.figure()
    plt.plot(grouped.index, grouped.values)
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Monthly Revenue Trend")
    plt.tight_layout()
    return plt


def profit_by_product_chart(df: pd.DataFrame):
    grouped = df.groupby("Product")["Profit"].sum()

    plt.figure()
    grouped.plot(kind="bar")
    plt.xlabel("Product")
    plt.ylabel("Profit")
    plt.title("Profit by Product")
    plt.tight_layout()
    return plt


def revenue_contribution_pie(df: pd.DataFrame):
    grouped = df.groupby("Product")["Revenue"].sum()

    plt.figure()
    plt.pie(grouped.values, labels=grouped.index, autopct="%1.1f%%")
    plt.title("Revenue Contribution by Product")
    plt.tight_layout()
    return plt
