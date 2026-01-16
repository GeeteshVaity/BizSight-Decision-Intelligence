"""
BizSight - Trend Analysis Module
File: analysis/trends.py
Author: Dhruv

This module contains pure functions for analyzing trends in business data.
Identifies patterns like growth, decline, stability over time periods.
No prints, only returns.

Required DataFrame columns: date, product_name, quantity, selling_price, revenue, cost, profit
"""

import pandas as pd
import numpy as np


def revenue_trend(df):
    """
    Analyze revenue trend over time.
    Determines if revenue is increasing, decreasing, or stable.
    
    Args:
        df (DataFrame): Business data with 'date' and 'revenue' columns
        
    Returns:
        dict: {
            'trend': 'increasing' | 'decreasing' | 'stable',
            'change_percent': float,
            'total_change': float
        }
    """
    if df is None or df.empty:
        return {'trend': 'stable', 'change_percent': 0.0, 'total_change': 0.0}
    
    required_cols = ['date', 'revenue']
    if not all(col in df.columns for col in required_cols):
        return {'trend': 'stable', 'change_percent': 0.0, 'total_change': 0.0}
    
    # Sort by date and group by date
    df_sorted = df.sort_values('date')
    daily_revenue = df_sorted.groupby('date')['revenue'].sum().reset_index()
    
    if len(daily_revenue) < 2:
        return {'trend': 'stable', 'change_percent': 0.0, 'total_change': 0.0}
    
    # Get first and last revenue values
    first_revenue = daily_revenue['revenue'].iloc[0]
    last_revenue = daily_revenue['revenue'].iloc[-1]
    
    # Calculate change
    total_change = last_revenue - first_revenue
    
    if first_revenue == 0:
        change_percent = 0.0
    else:
        change_percent = (total_change / first_revenue) * 100
    
    # Determine trend (threshold: 5% change)
    if change_percent > 5:
        trend = 'increasing'
    elif change_percent < -5:
        trend = 'decreasing'
    else:
        trend = 'stable'
    
    return {
        'trend': trend,
        'change_percent': float(change_percent),
        'total_change': float(total_change)
    }


def profit_trend(df):
    """
    Analyze profit trend over time.
    Uses profit column if available, otherwise calculates (revenue - cost).
    
    Args:
        df (DataFrame): Business data with 'date' and 'profit' columns (or 'revenue', 'cost')
        
    Returns:
        dict: {
            'trend': 'increasing' | 'decreasing' | 'stable',
            'change_percent': float,
            'total_change': float
        }
    """
    if df is None or df.empty:
        return {'trend': 'stable', 'change_percent': 0.0, 'total_change': 0.0}
    
    # Check if profit column exists
    if 'profit' in df.columns:
        profit_col = 'profit'
    elif 'revenue' in df.columns and 'cost' in df.columns:
        # Calculate profit if not present
        df = df.copy()
        df['profit'] = df['revenue'] - df['cost']
        profit_col = 'profit'
    else:
        return {'trend': 'stable', 'change_percent': 0.0, 'total_change': 0.0}
    
    if 'date' not in df.columns:
        return {'trend': 'stable', 'change_percent': 0.0, 'total_change': 0.0}
    
    # Sort by date and group by date
    df_sorted = df.sort_values('date')
    daily_profit = df_sorted.groupby('date')[profit_col].sum().reset_index()
    
    if len(daily_profit) < 2:
        return {'trend': 'stable', 'change_percent': 0.0, 'total_change': 0.0}
    
    # Get first and last profit values
    first_profit = daily_profit[profit_col].iloc[0]
    last_profit = daily_profit[profit_col].iloc[-1]
    
    # Calculate change
    total_change = last_profit - first_profit
    
    if first_profit == 0:
        change_percent = 0.0
    else:
        change_percent = (total_change / abs(first_profit)) * 100
    
    # Determine trend
    if change_percent > 5:
        trend = 'increasing'
    elif change_percent < -5:
        trend = 'decreasing'
    else:
        trend = 'stable'
    
    return {
        'trend': trend,
        'change_percent': float(change_percent),
        'total_change': float(total_change)
    }


def growth_rate(df, period='overall'):
    """
    Calculate revenue growth rate.
    
    Args:
        df (DataFrame): Business data with 'date' and 'revenue' columns
        period (str): 'overall' or 'average' (for average daily growth)
        
    Returns:
        float: Growth rate as percentage
    """
    if df is None or df.empty:
        return 0.0
    
    required_cols = ['date', 'revenue']
    if not all(col in df.columns for col in required_cols):
        return 0.0
    
    # Sort by date and group by date
    df_sorted = df.sort_values('date')
    daily_revenue = df_sorted.groupby('date')['revenue'].sum().reset_index()
    
    if len(daily_revenue) < 2:
        return 0.0
    
    if period == 'overall':
        # Overall growth from first to last
        first_revenue = daily_revenue['revenue'].iloc[0]
        last_revenue = daily_revenue['revenue'].iloc[-1]
        
        if first_revenue == 0:
            return 0.0
        
        growth = ((last_revenue - first_revenue) / first_revenue) * 100
        return float(growth)
    
    elif period == 'average':
        # Average daily growth rate
        revenues = daily_revenue['revenue'].values
        growth_rates = []
        
        for i in range(1, len(revenues)):
            if revenues[i-1] != 0:
                daily_growth = ((revenues[i] - revenues[i-1]) / revenues[i-1]) * 100
                growth_rates.append(daily_growth)
        
        if not growth_rates:
            return 0.0
        
        return float(np.mean(growth_rates))
    
    return 0.0


def detect_consecutive_losses(df, threshold=3):
    """
    Detect if there are consecutive days/periods with losses.
    
    Args:
        df (DataFrame): Business data with 'date' and 'profit' columns (or 'revenue', 'cost')
        threshold (int): Number of consecutive loss days to flag as risk
        
    Returns:
        dict: {
            'has_consecutive_losses': bool,
            'max_consecutive_days': int,
            'loss_periods': list of dates
        }
    """
    if df is None or df.empty:
        return {
            'has_consecutive_losses': False,
            'max_consecutive_days': 0,
            'loss_periods': []
        }
    
    # Check if profit column exists
    if 'profit' in df.columns:
        df_copy = df.copy()
        profit_col = 'profit'
    elif 'revenue' in df.columns and 'cost' in df.columns:
        df_copy = df.copy()
        df_copy['profit'] = df_copy['revenue'] - df_copy['cost']
        profit_col = 'profit'
    else:
        return {
            'has_consecutive_losses': False,
            'max_consecutive_days': 0,
            'loss_periods': []
        }
    
    if 'date' not in df_copy.columns:
        return {
            'has_consecutive_losses': False,
            'max_consecutive_days': 0,
            'loss_periods': []
        }
    
    # Sort by date and group by date
    df_sorted = df_copy.sort_values('date')
    daily_profit = df_sorted.groupby('date')[profit_col].sum().reset_index()
    
    # Find consecutive losses
    consecutive = 0
    max_consecutive = 0
    loss_dates = []
    current_streak_dates = []
    
    for idx, row in daily_profit.iterrows():
        if row[profit_col] < 0:
            consecutive += 1
            current_streak_dates.append(str(row['date']))
            max_consecutive = max(max_consecutive, consecutive)
        else:
            if consecutive >= threshold:
                loss_dates.extend(current_streak_dates)
            consecutive = 0
            current_streak_dates = []
    
    # Check last streak
    if consecutive >= threshold:
        loss_dates.extend(current_streak_dates)
    
    has_losses = max_consecutive >= threshold
    
    return {
        'has_consecutive_losses': has_losses,
        'max_consecutive_days': int(max_consecutive),
        'loss_periods': loss_dates
    }


def product_trend_ranking(df):
    """
    Rank products by their revenue trend (which products are growing/declining).
    
    Args:
        df (DataFrame): Business data with 'date', 'product_name', 'revenue' columns
        
    Returns:
        list: List of dicts sorted by growth rate, each containing:
              {'product': str, 'growth_rate': float, 'trend': str}
    """
    if df is None or df.empty:
        return []
    
    required_cols = ['date', 'product_name', 'revenue']
    if not all(col in df.columns for col in required_cols):
        return []
    
    products = df['product_name'].unique()
    rankings = []
    
    for product in products:
        product_df = df[df['product_name'] == product].copy()
        
        # Sort by date
        product_df = product_df.sort_values('date')
        daily_revenue = product_df.groupby('date')['revenue'].sum().reset_index()
        
        if len(daily_revenue) < 2:
            continue
        
        # Calculate growth rate for this product
        first_rev = daily_revenue['revenue'].iloc[0]
        last_rev = daily_revenue['revenue'].iloc[-1]
        
        if first_rev == 0:
            growth = 0.0
        else:
            growth = ((last_rev - first_rev) / first_rev) * 100
        
        # Determine trend
        if growth > 5:
            trend = 'growing'
        elif growth < -5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        rankings.append({
            'product': product,
            'growth_rate': float(growth),
            'trend': trend
        })
    
    # Sort by growth rate (highest first)
    rankings.sort(key=lambda x: x['growth_rate'], reverse=True)
    
    return rankings


def get_all_trends(df):
    """
    Get all trend analysis results in one dictionary.
    Useful for generating comprehensive trend reports.
    
    Args:
        df (DataFrame): Business data
        
    Returns:
        dict: All trend analysis results
    """
    return {
        'revenue_trend': revenue_trend(df),
        'profit_trend': profit_trend(df),
        'overall_growth_rate': growth_rate(df, 'overall'),
        'average_growth_rate': growth_rate(df, 'average'),
        'consecutive_losses': detect_consecutive_losses(df),
        'product_rankings': product_trend_ranking(df)
    }