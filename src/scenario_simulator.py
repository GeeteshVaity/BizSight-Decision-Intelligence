"""
Scenario Simulator Module
Simulates what-if scenarios by adjusting revenue or cost parameters
"""

import pandas as pd
import numpy as np


class ScenarioSimulator:
    """
    Simulate what-if scenarios for business decisions
    """
    
    def __init__(self, data):
        """
        Initialize the ScenarioSimulator
        
        Args:
            data (pd.DataFrame): Original business data
        """
        self.original_data = data.copy()
        self.scenarios = []
    
    def simulate_revenue_change(self, percentage_change, scenario_name=None):
        """
        Simulate a percentage change in revenue
        
        Args:
            percentage_change (float): Percentage change in revenue (e.g., 10 for +10%, -5 for -5%)
            scenario_name (str): Name for the scenario
            
        Returns:
            dict: Scenario results
        """
        if scenario_name is None:
            scenario_name = f"Revenue {'+' if percentage_change >= 0 else ''}{percentage_change}%"
        
        # Create modified data
        simulated_data = self.original_data.copy()
        simulated_data['revenue'] = simulated_data['revenue'] * (1 + percentage_change / 100)
        simulated_data['profit'] = simulated_data['revenue'] - simulated_data['cost']
        
        # Calculate impact
        scenario_result = self._calculate_scenario_impact(
            self.original_data,
            simulated_data,
            scenario_name,
            'revenue'
        )
        
        self.scenarios.append(scenario_result)
        return scenario_result
    
    def simulate_cost_change(self, percentage_change, scenario_name=None):
        """
        Simulate a percentage change in cost
        
        Args:
            percentage_change (float): Percentage change in cost (e.g., 10 for +10%, -5 for -5%)
            scenario_name (str): Name for the scenario
            
        Returns:
            dict: Scenario results
        """
        if scenario_name is None:
            scenario_name = f"Cost {'+' if percentage_change >= 0 else ''}{percentage_change}%"
        
        # Create modified data
        simulated_data = self.original_data.copy()
        simulated_data['cost'] = simulated_data['cost'] * (1 + percentage_change / 100)
        simulated_data['profit'] = simulated_data['revenue'] - simulated_data['cost']
        
        # Calculate impact
        scenario_result = self._calculate_scenario_impact(
            self.original_data,
            simulated_data,
            scenario_name,
            'cost'
        )
        
        self.scenarios.append(scenario_result)
        return scenario_result
    
    def simulate_combined_change(self, revenue_change, cost_change, scenario_name=None):
        """
        Simulate combined changes in both revenue and cost
        
        Args:
            revenue_change (float): Percentage change in revenue
            cost_change (float): Percentage change in cost
            scenario_name (str): Name for the scenario
            
        Returns:
            dict: Scenario results
        """
        if scenario_name is None:
            scenario_name = f"Revenue {'+' if revenue_change >= 0 else ''}{revenue_change}%, Cost {'+' if cost_change >= 0 else ''}{cost_change}%"
        
        # Create modified data
        simulated_data = self.original_data.copy()
        simulated_data['revenue'] = simulated_data['revenue'] * (1 + revenue_change / 100)
        simulated_data['cost'] = simulated_data['cost'] * (1 + cost_change / 100)
        simulated_data['profit'] = simulated_data['revenue'] - simulated_data['cost']
        
        # Calculate impact
        scenario_result = self._calculate_scenario_impact(
            self.original_data,
            simulated_data,
            scenario_name,
            'combined'
        )
        
        self.scenarios.append(scenario_result)
        return scenario_result
    
    def _calculate_scenario_impact(self, original_data, simulated_data, scenario_name, change_type):
        """
        Calculate the impact of a scenario
        
        Args:
            original_data (pd.DataFrame): Original data
            simulated_data (pd.DataFrame): Simulated data
            scenario_name (str): Name of the scenario
            change_type (str): Type of change ('revenue', 'cost', or 'combined')
            
        Returns:
            dict: Scenario impact analysis
        """
        # Calculate original metrics
        original_profit = original_data['revenue'] - original_data['cost']
        original_total_revenue = original_data['revenue'].sum()
        original_total_cost = original_data['cost'].sum()
        original_total_profit = original_profit.sum()
        
        # Calculate simulated metrics
        simulated_total_revenue = simulated_data['revenue'].sum()
        simulated_total_cost = simulated_data['cost'].sum()
        simulated_total_profit = simulated_data['profit'].sum()
        
        # Calculate changes
        revenue_change = simulated_total_revenue - original_total_revenue
        cost_change = simulated_total_cost - original_total_cost
        profit_change = simulated_total_profit - original_total_profit
        
        # Calculate percentage changes
        revenue_pct_change = (revenue_change / original_total_revenue * 100) if original_total_revenue != 0 else 0
        cost_pct_change = (cost_change / original_total_cost * 100) if original_total_cost != 0 else 0
        profit_pct_change = (profit_change / original_total_profit * 100) if original_total_profit != 0 else 0
        
        # Calculate profit margins
        original_margin = (original_total_profit / original_total_revenue * 100) if original_total_revenue != 0 else 0
        simulated_margin = (simulated_total_profit / simulated_total_revenue * 100) if simulated_total_revenue != 0 else 0
        
        scenario_result = {
            'scenario_name': scenario_name,
            'change_type': change_type,
            'original': {
                'total_revenue': original_total_revenue,
                'total_cost': original_total_cost,
                'total_profit': original_total_profit,
                'profit_margin': original_margin
            },
            'simulated': {
                'total_revenue': simulated_total_revenue,
                'total_cost': simulated_total_cost,
                'total_profit': simulated_total_profit,
                'profit_margin': simulated_margin
            },
            'impact': {
                'revenue_change': revenue_change,
                'revenue_pct_change': revenue_pct_change,
                'cost_change': cost_change,
                'cost_pct_change': cost_pct_change,
                'profit_change': profit_change,
                'profit_pct_change': profit_pct_change,
                'margin_change': simulated_margin - original_margin
            },
            'data': simulated_data
        }
        
        return scenario_result
    
    def compare_scenarios(self):
        """
        Compare all simulated scenarios
        
        Returns:
            pd.DataFrame: Comparison table of all scenarios
        """
        if not self.scenarios:
            print("No scenarios to compare. Run simulations first.")
            return None
        
        comparison_data = []
        
        # Add baseline
        original_profit = self.original_data['revenue'] - self.original_data['cost']
        baseline = {
            'Scenario': 'Baseline (Original)',
            'Total Revenue': self.original_data['revenue'].sum(),
            'Total Cost': self.original_data['cost'].sum(),
            'Total Profit': original_profit.sum(),
            'Profit Margin (%)': (original_profit.sum() / self.original_data['revenue'].sum() * 100) if self.original_data['revenue'].sum() != 0 else 0
        }
        comparison_data.append(baseline)
        
        # Add scenarios
        for scenario in self.scenarios:
            row = {
                'Scenario': scenario['scenario_name'],
                'Total Revenue': scenario['simulated']['total_revenue'],
                'Total Cost': scenario['simulated']['total_cost'],
                'Total Profit': scenario['simulated']['total_profit'],
                'Profit Margin (%)': scenario['simulated']['profit_margin']
            }
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        return comparison_df
    
    def get_best_scenario(self, metric='profit'):
        """
        Get the best performing scenario based on a metric
        
        Args:
            metric (str): Metric to optimize ('profit', 'revenue', or 'margin')
            
        Returns:
            dict: Best scenario
        """
        if not self.scenarios:
            print("No scenarios to compare. Run simulations first.")
            return None
        
        metric_map = {
            'profit': lambda s: s['simulated']['total_profit'],
            'revenue': lambda s: s['simulated']['total_revenue'],
            'margin': lambda s: s['simulated']['profit_margin']
        }
        
        if metric not in metric_map:
            raise ValueError(f"Invalid metric: {metric}. Choose from 'profit', 'revenue', or 'margin'.")
        
        best_scenario = max(self.scenarios, key=metric_map[metric])
        return best_scenario
