"""
BizSight - Risk Detection Module
File: intelligence/risk_detector.py
Author: Dhruv

This module contains rule-based risk detection functions.
Identifies financial risks and warning signals in business data.
No prints, only returns.

Required DataFrame columns: date, product_name, quantity, selling_price, revenue, cost, profit
"""

import pandas as pd
import numpy as np


def detect_continuous_losses(df, threshold_days=3):
    """
    Detect if business has continuous losses for consecutive days.
    
    Args:
        df (DataFrame): Business data with 'date' and 'profit' columns
        threshold_days (int): Number of consecutive loss days to trigger warning
        
    Returns:
        dict: {
            'risk_detected': bool,
            'severity': 'low' | 'medium' | 'high',
            'consecutive_loss_days': int,
            'total_loss_amount': float,
            'loss_dates': list,
            'message': str
        }
    """
    if df is None or df.empty:
        return {
            'risk_detected': False,
            'severity': 'low',
            'consecutive_loss_days': 0,
            'total_loss_amount': 0.0,
            'loss_dates': [],
            'message': 'No data available'
        }
    
    # Check if profit column exists, otherwise calculate it
    if 'profit' in df.columns:
        df_copy = df.copy()
    elif 'revenue' in df.columns and 'cost' in df.columns:
        df_copy = df.copy()
        df_copy['profit'] = df_copy['revenue'] - df_copy['cost']
    else:
        return {
            'risk_detected': False,
            'severity': 'low',
            'consecutive_loss_days': 0,
            'total_loss_amount': 0.0,
            'loss_dates': [],
            'message': 'Required columns not found'
        }
    
    if 'date' not in df_copy.columns:
        return {
            'risk_detected': False,
            'severity': 'low',
            'consecutive_loss_days': 0,
            'total_loss_amount': 0.0,
            'loss_dates': [],
            'message': 'Date column not found'
        }
    
    # Group by date and calculate daily profit
    df_sorted = df_copy.sort_values('date')
    daily_profit = df_sorted.groupby('date')['profit'].sum().reset_index()
    
    # Find consecutive losses
    consecutive = 0
    max_consecutive = 0
    current_streak_dates = []
    max_streak_dates = []
    total_loss = 0.0
    
    for idx, row in daily_profit.iterrows():
        if row['profit'] < 0:
            consecutive += 1
            current_streak_dates.append(str(row['date']))
            total_loss += abs(row['profit'])
            
            if consecutive > max_consecutive:
                max_consecutive = consecutive
                max_streak_dates = current_streak_dates.copy()
        else:
            consecutive = 0
            current_streak_dates = []
    
    # Determine risk
    risk_detected = max_consecutive >= threshold_days
    
    # Determine severity
    if max_consecutive >= 7:
        severity = 'high'
    elif max_consecutive >= 5:
        severity = 'medium'
    elif max_consecutive >= threshold_days:
        severity = 'low'
    else:
        severity = 'low'
    
    # Generate message
    if risk_detected:
        message = f"Warning: {max_consecutive} consecutive days of losses detected. Total loss: ${total_loss:,.2f}"
    else:
        message = "No continuous loss pattern detected"
    
    return {
        'risk_detected': risk_detected,
        'severity': severity,
        'consecutive_loss_days': int(max_consecutive),
        'total_loss_amount': float(total_loss),
        'loss_dates': max_streak_dates,
        'message': message
    }


def detect_declining_revenue(df, threshold_percent=-10):
    """
    Detect if revenue is declining over time.
    
    Args:
        df (DataFrame): Business data with 'date' and 'revenue' columns
        threshold_percent (float): Percentage decline to trigger warning (negative value)
        
    Returns:
        dict: {
            'risk_detected': bool,
            'severity': 'low' | 'medium' | 'high',
            'decline_percent': float,
            'revenue_change': float,
            'message': str
        }
    """
    if df is None or df.empty:
        return {
            'risk_detected': False,
            'severity': 'low',
            'decline_percent': 0.0,
            'revenue_change': 0.0,
            'message': 'No data available'
        }
    
    required_cols = ['date', 'revenue']
    if not all(col in df.columns for col in required_cols):
        return {
            'risk_detected': False,
            'severity': 'low',
            'decline_percent': 0.0,
            'revenue_change': 0.0,
            'message': 'Required columns not found'
        }
    
    # Group by date and calculate daily revenue
    df_sorted = df.sort_values('date')
    daily_revenue = df_sorted.groupby('date')['revenue'].sum().reset_index()
    
    if len(daily_revenue) < 2:
        return {
            'risk_detected': False,
            'severity': 'low',
            'decline_percent': 0.0,
            'revenue_change': 0.0,
            'message': 'Insufficient data for trend analysis'
        }
    
    # Calculate change from first to last
    first_revenue = daily_revenue['revenue'].iloc[0]
    last_revenue = daily_revenue['revenue'].iloc[-1]
    
    revenue_change = last_revenue - first_revenue
    
    if first_revenue == 0:
        decline_percent = 0.0
    else:
        decline_percent = (revenue_change / first_revenue) * 100
    
    # Determine risk
    risk_detected = decline_percent <= threshold_percent
    
    # Determine severity
    if decline_percent <= -20:
        severity = 'high'
    elif decline_percent <= -15:
        severity = 'medium'
    elif decline_percent <= threshold_percent:
        severity = 'low'
    else:
        severity = 'low'
    
    # Generate message
    if risk_detected:
        message = f"Warning: Revenue declining by {abs(decline_percent):.2f}%. Change: ${revenue_change:,.2f}"
    else:
        message = "Revenue trend is stable or growing"
    
    return {
        'risk_detected': risk_detected,
        'severity': severity,
        'decline_percent': float(decline_percent),
        'revenue_change': float(revenue_change),
        'message': message
    }


def detect_high_cost_ratio(df, threshold_ratio=0.8):
    """
    Detect if cost-to-revenue ratio is too high (low profit margin).
    
    Args:
        df (DataFrame): Business data with 'revenue' and 'cost' columns
        threshold_ratio (float): Cost/Revenue ratio threshold (0.8 = 80% costs)
        
    Returns:
        dict: {
            'risk_detected': bool,
            'severity': 'low' | 'medium' | 'high',
            'cost_ratio': float,
            'profit_margin': float,
            'message': str
        }
    """
    if df is None or df.empty:
        return {
            'risk_detected': False,
            'severity': 'low',
            'cost_ratio': 0.0,
            'profit_margin': 0.0,
            'message': 'No data available'
        }
    
    required_cols = ['revenue', 'cost']
    if not all(col in df.columns for col in required_cols):
        return {
            'risk_detected': False,
            'severity': 'low',
            'cost_ratio': 0.0,
            'profit_margin': 0.0,
            'message': 'Required columns not found'
        }
    
    total_revenue = df['revenue'].sum()
    total_cost = df['cost'].sum()
    
    if total_revenue == 0:
        return {
            'risk_detected': False,
            'severity': 'low',
            'cost_ratio': 0.0,
            'profit_margin': 0.0,
            'message': 'No revenue data'
        }
    
    cost_ratio = total_cost / total_revenue
    profit_margin = ((total_revenue - total_cost) / total_revenue) * 100
    
    # Determine risk
    risk_detected = cost_ratio >= threshold_ratio
    
    # Determine severity
    if cost_ratio >= 0.95:
        severity = 'high'
    elif cost_ratio >= 0.85:
        severity = 'medium'
    elif cost_ratio >= threshold_ratio:
        severity = 'low'
    else:
        severity = 'low'
    
    # Generate message
    if risk_detected:
        message = f"Warning: High cost ratio {cost_ratio*100:.1f}%. Profit margin only {profit_margin:.1f}%"
    else:
        message = f"Cost ratio is healthy at {cost_ratio*100:.1f}%"
    
    return {
        'risk_detected': risk_detected,
        'severity': severity,
        'cost_ratio': float(cost_ratio),
        'profit_margin': float(profit_margin),
        'message': message
    }


def detect_low_profit_margin(df, threshold_margin=10.0):
    """
    Detect if overall profit margin is too low.
    
    Args:
        df (DataFrame): Business data with 'revenue' and 'cost' columns
        threshold_margin (float): Minimum acceptable profit margin percentage
        
    Returns:
        dict: {
            'risk_detected': bool,
            'severity': 'low' | 'medium' | 'high',
            'profit_margin': float,
            'total_profit': float,
            'message': str
        }
    """
    if df is None or df.empty:
        return {
            'risk_detected': False,
            'severity': 'low',
            'profit_margin': 0.0,
            'total_profit': 0.0,
            'message': 'No data available'
        }
    
    required_cols = ['revenue', 'cost']
    if not all(col in df.columns for col in required_cols):
        return {
            'risk_detected': False,
            'severity': 'low',
            'profit_margin': 0.0,
            'total_profit': 0.0,
            'message': 'Required columns not found'
        }
    
    total_revenue = df['revenue'].sum()
    total_cost = df['cost'].sum()
    total_profit = total_revenue - total_cost
    
    if total_revenue == 0:
        return {
            'risk_detected': False,
            'severity': 'low',
            'profit_margin': 0.0,
            'total_profit': 0.0,
            'message': 'No revenue data'
        }
    
    profit_margin = (total_profit / total_revenue) * 100
    
    # Determine risk
    risk_detected = profit_margin < threshold_margin
    
    # Determine severity
    if profit_margin < 0:
        severity = 'high'
    elif profit_margin < 5:
        severity = 'medium'
    elif profit_margin < threshold_margin:
        severity = 'low'
    else:
        severity = 'low'
    
    # Generate message
    if risk_detected:
        if profit_margin < 0:
            message = f"Critical: Business is making losses. Profit margin: {profit_margin:.2f}%"
        else:
            message = f"Warning: Low profit margin {profit_margin:.2f}% (threshold: {threshold_margin}%)"
    else:
        message = f"Profit margin is healthy at {profit_margin:.2f}%"
    
    return {
        'risk_detected': risk_detected,
        'severity': severity,
        'profit_margin': float(profit_margin),
        'total_profit': float(total_profit),
        'message': message
    }


def detect_underperforming_products(df, threshold_margin=5.0):
    """
    Detect products with low or negative profit margins.
    
    Args:
        df (DataFrame): Business data with 'product_name', 'revenue', 'cost' columns
        threshold_margin (float): Minimum acceptable profit margin percentage per product
        
    Returns:
        dict: {
            'risk_detected': bool,
            'underperforming_products': list of dicts,
            'count': int,
            'message': str
        }
    """
    if df is None or df.empty:
        return {
            'risk_detected': False,
            'underperforming_products': [],
            'count': 0,
            'message': 'No data available'
        }
    
    required_cols = ['product_name', 'revenue', 'cost']
    if not all(col in df.columns for col in required_cols):
        return {
            'risk_detected': False,
            'underperforming_products': [],
            'count': 0,
            'message': 'Required columns not found'
        }
    
    # Calculate product-wise metrics
    product_summary = df.groupby('product_name').agg({
        'revenue': 'sum',
        'cost': 'sum'
    }).reset_index()
    
    underperforming = []
    
    for _, row in product_summary.iterrows():
        product = row['product_name']
        revenue = row['revenue']
        cost = row['cost']
        profit = revenue - cost
        
        if revenue == 0:
            continue
        
        margin = (profit / revenue) * 100
        
        if margin < threshold_margin:
            underperforming.append({
                'product': product,
                'profit_margin': float(margin),
                'profit': float(profit),
                'revenue': float(revenue),
                'cost': float(cost)
            })
    
    # Sort by margin (worst first)
    underperforming.sort(key=lambda x: x['profit_margin'])
    
    risk_detected = len(underperforming) > 0
    
    # Generate message
    if risk_detected:
        message = f"Warning: {len(underperforming)} product(s) with margins below {threshold_margin}%"
    else:
        message = "All products performing well"
    
    return {
        'risk_detected': risk_detected,
        'underperforming_products': underperforming,
        'count': len(underperforming),
        'message': message
    }


def get_all_risks(df):
    """
    Run all risk detection functions and return comprehensive risk report.
    
    Args:
        df (DataFrame): Business data
        
    Returns:
        dict: All risk detection results with overall risk summary
    """
    risks = {
        'continuous_losses': detect_continuous_losses(df),
        'declining_revenue': detect_declining_revenue(df),
        'high_cost_ratio': detect_high_cost_ratio(df),
        'low_profit_margin': detect_low_profit_margin(df),
        'underperforming_products': detect_underperforming_products(df)
    }
    
    # Count total risks detected
    total_risks = sum(1 for risk in risks.values() if risk.get('risk_detected', False))
    
    # Count by severity
    high_severity = sum(1 for risk in risks.values() if risk.get('severity') == 'high')
    medium_severity = sum(1 for risk in risks.values() if risk.get('severity') == 'medium')
    low_severity = sum(1 for risk in risks.values() if risk.get('severity') == 'low' and risk.get('risk_detected', False))
    
    # Overall risk level
    if high_severity > 0:
        overall_risk = 'high'
    elif medium_severity > 0:
        overall_risk = 'medium'
    elif low_severity > 0:
        overall_risk = 'low'
    else:
        overall_risk = 'none'
    
    risks['summary'] = {
        'total_risks_detected': total_risks,
        'high_severity_count': high_severity,
        'medium_severity_count': medium_severity,
        'low_severity_count': low_severity,
        'overall_risk_level': overall_risk
    }
    
    return risks