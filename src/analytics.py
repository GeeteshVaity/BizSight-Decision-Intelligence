"""
Analytics Module
Analyzes business data for revenue, cost, profit, and trends
"""

import pandas as pd
import numpy as np


class BusinessAnalytics:
    """
    Perform various business analytics on the data
    """
    
    def __init__(self, data):
        """
        Initialize the BusinessAnalytics
        
        Args:
            data (pd.DataFrame): Business data with date, revenue, and cost columns
        """
        self.data = data.copy()
        self._calculate_profit()
    
    def _calculate_profit(self):
        """
        Calculate profit from revenue and cost
        """
        self.data['profit'] = self.data['revenue'] - self.data['cost']
    
    def get_summary_statistics(self):
        """
        Get summary statistics for revenue, cost, and profit
        
        Returns:
            dict: Summary statistics
        """
        summary = {
            'revenue': {
                'total': self.data['revenue'].sum(),
                'mean': self.data['revenue'].mean(),
                'median': self.data['revenue'].median(),
                'std': self.data['revenue'].std(),
                'min': self.data['revenue'].min(),
                'max': self.data['revenue'].max()
            },
            'cost': {
                'total': self.data['cost'].sum(),
                'mean': self.data['cost'].mean(),
                'median': self.data['cost'].median(),
                'std': self.data['cost'].std(),
                'min': self.data['cost'].min(),
                'max': self.data['cost'].max()
            },
            'profit': {
                'total': self.data['profit'].sum(),
                'mean': self.data['profit'].mean(),
                'median': self.data['profit'].median(),
                'std': self.data['profit'].std(),
                'min': self.data['profit'].min(),
                'max': self.data['profit'].max()
            }
        }
        
        return summary
    
    def calculate_profit_margin(self):
        """
        Calculate profit margin percentage
        
        Returns:
            pd.Series: Profit margin for each record
        """
        # Avoid division by zero
        profit_margin = np.where(
            self.data['revenue'] != 0,
            (self.data['profit'] / self.data['revenue']) * 100,
            0
        )
        
        return pd.Series(profit_margin, index=self.data.index)
    
    def analyze_trends(self, window=3):
        """
        Analyze trends in revenue, cost, and profit using moving averages
        
        Args:
            window (int): Window size for moving average (default: 3)
            
        Returns:
            dict: Trend analysis results
        """
        trends = {
            'revenue_trend': self.data['revenue'].rolling(window=window).mean(),
            'cost_trend': self.data['cost'].rolling(window=window).mean(),
            'profit_trend': self.data['profit'].rolling(window=window).mean()
        }
        
        # Calculate trend direction (increasing/decreasing)
        trends['revenue_direction'] = self._calculate_trend_direction(trends['revenue_trend'])
        trends['cost_direction'] = self._calculate_trend_direction(trends['cost_trend'])
        trends['profit_direction'] = self._calculate_trend_direction(trends['profit_trend'])
        
        return trends
    
    def _calculate_trend_direction(self, series):
        """
        Calculate trend direction from a series
        
        Args:
            series (pd.Series): Time series data
            
        Returns:
            str: 'increasing', 'decreasing', or 'stable'
        """
        # Get first and last non-null values
        valid_values = series.dropna()
        
        if len(valid_values) < 2:
            return 'insufficient_data'
        
        first_value = valid_values.iloc[0]
        last_value = valid_values.iloc[-1]
        
        # Handle zero first_value to avoid division by zero
        if first_value == 0:
            if last_value > 0:
                return 'increasing'
            elif last_value < 0:
                return 'decreasing'
            else:
                return 'stable'
        
        # Calculate percentage change
        pct_change = ((last_value - first_value) / first_value) * 100
        
        if pct_change > 5:
            return 'increasing'
        elif pct_change < -5:
            return 'decreasing'
        else:
            return 'stable'
    
    def get_monthly_aggregates(self):
        """
        Get monthly aggregated statistics
        
        Returns:
            pd.DataFrame: Monthly aggregated data
        """
        # Create a copy with month column
        monthly_data = self.data.copy()
        monthly_data['month'] = monthly_data['date'].dt.to_period('M')
        
        # Aggregate by month
        monthly_agg = monthly_data.groupby('month').agg({
            'revenue': 'sum',
            'cost': 'sum',
            'profit': 'sum'
        }).reset_index()
        
        monthly_agg['month'] = monthly_agg['month'].astype(str)
        
        return monthly_agg
    
    def get_top_performing_periods(self, metric='profit', top_n=5):
        """
        Get top performing periods based on a metric
        
        Args:
            metric (str): Metric to use ('profit', 'revenue', or 'cost')
            top_n (int): Number of top periods to return
            
        Returns:
            pd.DataFrame: Top performing periods
        """
        if metric not in ['profit', 'revenue', 'cost']:
            raise ValueError(f"Invalid metric: {metric}. Choose from 'profit', 'revenue', or 'cost'.")
        
        top_periods = self.data.nlargest(top_n, metric)[['date', 'revenue', 'cost', 'profit']]
        
        return top_periods
