import matplotlib.pyplot as plt
import pandas as pd


def revenue_trend_chart(df: pd.DataFrame):
    """
    Create a line chart showing monthly revenue trends over time.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing at least the following columns:
        - ``date``: Date values that can be converted to datetime.
        - ``revenue``: Numeric revenue values associated with each date.
        Additional columns in the DataFrame are ignored by this function.

    Returns
    -------
    matplotlib.figure.Figure
        A matplotlib Figure object configured to display a line chart
        of monthly revenue trends.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    grouped = df.groupby(df["date"].dt.to_period("M"))["revenue"].sum()
    grouped.index = grouped.index.to_timestamp()

    fig = plt.figure()
    plt.plot(grouped.index, grouped.values)
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Monthly Revenue Trend")
    plt.tight_layout()
    return fig


def profit_by_product_chart(df: pd.DataFrame):
    """
    Create a bar chart showing total profit by product.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing at least the following columns:
        - ``product``: Categorical or string identifiers for each product.
        - ``profit``: Numeric profit values associated with each product.
        Additional columns in the DataFrame are ignored by this function.

    Returns
    -------
    matplotlib.figure.Figure
        A matplotlib Figure object configured to display a bar chart
        of profit by product.
    """
    grouped = df.groupby("product")["profit"].sum()

    fig = plt.figure()
    grouped.plot(kind="bar")
    plt.xlabel("Product")
    plt.ylabel("Profit")
    plt.title("Profit by Product")
    plt.tight_layout()
    return fig


def revenue_contribution_pie(df: pd.DataFrame):
    """
    Create a pie chart showing each product's contribution to total revenue.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing at least the following columns:
        - ``product``: Categorical or string identifiers for each product.
        - ``revenue``: Numeric revenue values associated with each product.
        Additional columns in the DataFrame are ignored by this function.

    Returns
    -------
    matplotlib.figure.Figure
        A matplotlib Figure object configured to display a pie chart
        of revenue contribution by product.
    """
    grouped = df.groupby("product")["revenue"].sum()

    fig = plt.figure()
    plt.pie(grouped.values, labels=grouped.index, autopct="%1.1f%%")
    plt.title("Revenue Contribution by Product")
    plt.tight_layout()
    return fig
