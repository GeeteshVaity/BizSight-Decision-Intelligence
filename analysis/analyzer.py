"""
BizSight - Business Calculations Module
File: analysis/analyzer.py
Author: Dhruv

This module contains pure functions for business calculations.
All functions take a DataFrame as input and return calculated values.
No prints, only returns.

Required DataFrame columns: date, product_name, quantity, selling_price, revenue, cost, profit
"""

import pandas as pd


def total_revenue(df):
    """
    Calculate total revenue from the business data.
    
    Args:
        df (DataFrame): Business data with 'revenue' column
        
    Returns:
        float: Total revenue across all records
    """
    if df is None or df.empty:
        return 0.0
    
    if 'revenue' not in df.columns:
        return 0.0
    
    return float(df['revenue'].sum())


def total_cost(df):
    """
    Calculate total cost from the business data.
    
    Args:
        df (DataFrame): Business data with 'cost' column
        
    Returns:
        float: Total cost across all records
    """
    if df is None or df.empty:
        return 0.0
    
    if 'cost' not in df.columns:
        return 0.0
    
    return float(df['cost'].sum())


def total_profit(df):
    """
    Calculate total profit (revenue - cost).
    
    Args:
        df (DataFrame): Business data with 'profit' column (or 'revenue' and 'cost')
        
    Returns:
        float: Total profit (can be negative if loss)
    """
    if df is None or df.empty:
        return 0.0
    
    # If profit column exists, use it directly
    if 'profit' in df.columns:
        return float(df['profit'].sum())
    
    # Otherwise calculate from revenue and cost
    revenue = total_revenue(df)
    cost = total_cost(df)
    
    return revenue - cost


def profit_margin(df):
    """
    Calculate profit margin percentage.
    Formula: (Total Profit / Total Revenue) * 100
    
    Args:
        df (DataFrame): Business data with 'revenue' and 'cost' columns
        
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
        df (DataFrame): Business data with 'product_name', 'revenue', 'cost' columns
        
    Returns:
        dict: Dictionary with product names as keys and metrics as values
              Format: {
                  'Product A': {
                      'revenue': 1000.0,
                      'cost': 600.0,
                      'profit': 400.0,
                      'margin': 40.0,
                      'quantity': 10
                  }
              }
    """
    if df is None or df.empty:
        return {}
    
    required_cols = ['product_name', 'revenue', 'cost']
    if not all(col in df.columns for col in required_cols):
        return {}
    
    summary = {}
    
    # Prepare aggregation dictionary
    agg_dict = {
        'revenue': 'sum',
        'cost': 'sum'
    }
    
    # Add quantity if it exists
    if 'quantity' in df.columns:
        agg_dict['quantity'] = 'sum'
    
    # Add profit if it exists
    if 'profit' in df.columns:
        agg_dict['profit'] = 'sum'
    
    # Group by product and calculate metrics
    grouped = df.groupby('product_name').agg(agg_dict).reset_index()
    
    for _, row in grouped.iterrows():
        product = row['product_name']
        revenue = float(row['revenue'])
        cost = float(row['cost'])
        
        # Calculate or get profit
        if 'profit' in row:
            profit = float(row['profit'])
        else:
            profit = revenue - cost
        
        # Calculate margin for this product
        if revenue > 0:
            margin = (profit / revenue) * 100
        else:
            margin = 0.0
        
        product_data = {
            'revenue': revenue,
            'cost': cost,
            'profit': profit,
            'margin': margin
        }
        
        # Add quantity if available
        if 'quantity' in row:
            product_data['quantity'] = int(row['quantity'])
        
        summary[product] = product_data
    
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