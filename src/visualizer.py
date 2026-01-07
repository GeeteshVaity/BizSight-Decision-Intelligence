"""
Visualization Module
Creates visualizations for business data and analysis results
"""

import matplotlib.pyplot as plt
import numpy as np
import os


class Visualizer:
    """
    Create various visualizations for business intelligence
    """
    
    def __init__(self, output_dir='outputs'):
        """
        Initialize the Visualizer
        
        Args:
            output_dir (str): Directory to save visualizations
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Set style
        plt.style.use('default')
    
    def plot_revenue_cost_profit(self, data, save=True, show=False):
        """
        Plot revenue, cost, and profit over time
        
        Args:
            data (pd.DataFrame): Business data
            save (bool): Whether to save the plot
            show (bool): Whether to display the plot
            
        Returns:
            str: Path to saved figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate profit
        profit = data['revenue'] - data['cost']
        
        # Plot lines
        ax.plot(data['date'], data['revenue'], label='Revenue', marker='o', linewidth=2, color='green')
        ax.plot(data['date'], data['cost'], label='Cost', marker='s', linewidth=2, color='red')
        ax.plot(data['date'], profit, label='Profit', marker='^', linewidth=2, color='blue')
        
        # Formatting
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_title('Revenue, Cost, and Profit Over Time', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save or show
        filepath = None
        if save:
            filepath = os.path.join(self.output_dir, 'revenue_cost_profit.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath
    
    def plot_profit_margin(self, data, save=True, show=False):
        """
        Plot profit margin over time
        
        Args:
            data (pd.DataFrame): Business data
            save (bool): Whether to save the plot
            show (bool): Whether to display the plot
            
        Returns:
            str: Path to saved figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Calculate profit margin
        profit = data['revenue'] - data['cost']
        profit_margin = np.where(
            data['revenue'] != 0,
            (profit / data['revenue']) * 100,
            0
        )
        
        # Plot
        ax.plot(data['date'], profit_margin, marker='o', linewidth=2, color='purple')
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Break-even')
        
        # Formatting
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Profit Margin (%)', fontsize=12)
        ax.set_title('Profit Margin Over Time', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save or show
        filepath = None
        if save:
            filepath = os.path.join(self.output_dir, 'profit_margin.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath
    
    def plot_trends(self, data, trends, save=True, show=False):
        """
        Plot trends with moving averages
        
        Args:
            data (pd.DataFrame): Business data
            trends (dict): Trend analysis results
            save (bool): Whether to save the plot
            show (bool): Whether to display the plot
            
        Returns:
            str: Path to saved figure
        """
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # Revenue trend
        axes[0].plot(data['date'], data['revenue'], label='Actual Revenue', alpha=0.5, color='lightgreen')
        axes[0].plot(data['date'], trends['revenue_trend'], label='Trend', linewidth=2, color='darkgreen')
        axes[0].set_ylabel('Revenue ($)', fontsize=10)
        axes[0].set_title(f"Revenue Trend (Direction: {trends['revenue_direction']})", fontsize=12, fontweight='bold')
        axes[0].legend(loc='best', fontsize=9)
        axes[0].grid(True, alpha=0.3)
        
        # Cost trend
        axes[1].plot(data['date'], data['cost'], label='Actual Cost', alpha=0.5, color='lightcoral')
        axes[1].plot(data['date'], trends['cost_trend'], label='Trend', linewidth=2, color='darkred')
        axes[1].set_ylabel('Cost ($)', fontsize=10)
        axes[1].set_title(f"Cost Trend (Direction: {trends['cost_direction']})", fontsize=12, fontweight='bold')
        axes[1].legend(loc='best', fontsize=9)
        axes[1].grid(True, alpha=0.3)
        
        # Profit trend
        profit = data['revenue'] - data['cost']
        axes[2].plot(data['date'], profit, label='Actual Profit', alpha=0.5, color='lightblue')
        axes[2].plot(data['date'], trends['profit_trend'], label='Trend', linewidth=2, color='darkblue')
        axes[2].set_xlabel('Date', fontsize=10)
        axes[2].set_ylabel('Profit ($)', fontsize=10)
        axes[2].set_title(f"Profit Trend (Direction: {trends['profit_direction']})", fontsize=12, fontweight='bold')
        axes[2].legend(loc='best', fontsize=9)
        axes[2].grid(True, alpha=0.3)
        
        # Format x-axis
        for ax in axes:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Save or show
        filepath = None
        if save:
            filepath = os.path.join(self.output_dir, 'trends_analysis.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath
    
    def plot_monthly_comparison(self, monthly_data, save=True, show=False):
        """
        Plot monthly comparison bar chart
        
        Args:
            monthly_data (pd.DataFrame): Monthly aggregated data
            save (bool): Whether to save the plot
            show (bool): Whether to display the plot
            
        Returns:
            str: Path to saved figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(monthly_data))
        width = 0.25
        
        # Create bars
        bars1 = ax.bar(x - width, monthly_data['revenue'], width, label='Revenue', color='green', alpha=0.8)
        bars2 = ax.bar(x, monthly_data['cost'], width, label='Cost', color='red', alpha=0.8)
        bars3 = ax.bar(x + width, monthly_data['profit'], width, label='Profit', color='blue', alpha=0.8)
        
        # Formatting
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_title('Monthly Revenue, Cost, and Profit Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(monthly_data['month'], rotation=45, ha='right')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        # Save or show
        filepath = None
        if save:
            filepath = os.path.join(self.output_dir, 'monthly_comparison.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath
    
    def plot_risk_summary(self, risk_summary, save=True, show=False):
        """
        Plot risk summary visualization
        
        Args:
            risk_summary (dict): Risk summary from risk detector
            save (bool): Whether to save the plot
            show (bool): Whether to display the plot
            
        Returns:
            str: Path to saved figure
        """
        if risk_summary.get('total_risks', 0) == 0:
            print("No risks to visualize")
            return None
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart of severity distribution
        severity_counts = risk_summary['by_severity']
        non_zero_severity = {k: v for k, v in severity_counts.items() if v > 0}
        
        colors = {'critical': 'darkred', 'high': 'red', 'medium': 'orange', 'low': 'yellow'}
        pie_colors = [colors[k] for k in non_zero_severity.keys()]
        
        ax1.pie(non_zero_severity.values(), labels=non_zero_severity.keys(), autopct='%1.1f%%',
                colors=pie_colors, startangle=90)
        ax1.set_title('Risk Distribution by Severity', fontsize=12, fontweight='bold')
        
        # Bar chart of risk types
        risks = risk_summary['risks']
        risk_types = [r['type'] for r in risks]
        risk_counts = {}
        for rt in risk_types:
            risk_counts[rt] = risk_counts.get(rt, 0) + 1
        
        ax2.barh(list(risk_counts.keys()), list(risk_counts.values()), color='coral')
        ax2.set_xlabel('Count', fontsize=10)
        ax2.set_title('Risk Types Detected', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        # Save or show
        filepath = None
        if save:
            filepath = os.path.join(self.output_dir, 'risk_summary.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved: {filepath}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return filepath
