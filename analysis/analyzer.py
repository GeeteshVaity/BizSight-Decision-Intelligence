"""
BizSight - Business Calculations Module
File: analysis/analyzer.py
Author: Dhruv

This module contains pure functions for business calculations.
All functions take a DataFrame as input and return calculated values.
No prints, only returns.
"""

import pandas as pd


def total_revenue(df):
    """
    Calculate total revenue from the business data.
    
    Args:
        df (DataFrame): Business data with 'Revenue' column
        
    Returns:
        float: Total revenue across all records
    """
    if df is None or df.empty:
        return 0.0
    
    if 'Revenue' not in df.columns:
        return 0.0
    
    return float(df['Revenue'].sum())


def total_cost(df):
    """
    Calculate total cost from the business data.
    
    Args:
        df (DataFrame): Business data with 'Cost' column
        
    Returns:
        float: Total cost across all records
    """
    if df is None or df.empty:
        return 0.0
    
    if 'Cost' not in df.columns:
        return 0.0
    
    return float(df['Cost'].sum())


def total_profit(df):
    """
    Calculate total profit (Revenue - Cost).
    
    Args:
        df (DataFrame): Business data with 'Revenue' and 'Cost' columns
        
    Returns:
        float: Total profit (can be negative if loss)
    """
    if df is None or df.empty:
        return 0.0
    
    revenue = total_revenue(df)
    cost = total_cost(df)
    
    return revenue - cost


def profit_margin(df):
    """
    Calculate profit margin percentage.
    Formula: (Total Profit / Total Revenue) * 100
    
    Args:
        df (DataFrame): Business data with 'Revenue' and 'Cost' columns
        
    Returns:
        float: Profit margin as percentage (0-100)
    """
    if df is None or df.empty:
        return 0.0
    
    revenue = total_revenue(df)
    
    if revenue == 0:
        return 0.0
    
    profit = total_profit(df)
    margin = (profit / revenue) * 100
    
    return float(margin)


def product_wise_summary(df):
    """
    Generate product-wise business summary.
    Calculates revenue, cost, and profit for each product.
    
    Args:
        df (DataFrame): Business data with 'Product', 'Revenue', 'Cost' columns
        
    Returns:
        dict: Dictionary with product names as keys and metrics as values
              Format: {
                  'Product A': {
                      'revenue': 1000.0,
                      'cost': 600.0,
                      'profit': 400.0,
                      'margin': 40.0
                  }
              }
    """
    if df is None or df.empty:
        return {}
    
    required_cols = ['Product', 'Revenue', 'Cost']
    if not all(col in df.columns for col in required_cols):
        return {}
    
    summary = {}
    
    # Group by product and calculate metrics
    grouped = df.groupby('Product').agg({
        'Revenue': 'sum',
        'Cost': 'sum'
    }).reset_index()
    
    for _, row in grouped.iterrows():
        product = row['Product']
        revenue = float(row['Revenue'])
        cost = float(row['Cost'])
        profit = revenue - cost
        
        # Calculate margin for this product
        if revenue > 0:
            margin = (profit / revenue) * 100
        else:
            margin = 0.0
        
        summary[product] = {
            'revenue': revenue,
            'cost': cost,
            'profit': profit,
            'margin': margin
        }
    
    return summary


# Additional helper function for getting overall metrics dictionary
def get_all_metrics(df):
    """
    Get all business metrics in one dictionary.
    Useful for generating reports or displaying dashboard.
    
    Args:
        df (DataFrame): Business data
        
    Returns:
        dict: All calculated metrics
    """
    return {
        'total_revenue': total_revenue(df),
        'total_cost': total_cost(df),
        'total_profit': total_profit(df),
        'profit_margin': profit_margin(df),
        'product_summary': product_wise_summary(df)
    }