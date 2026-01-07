"""
Risk Detection Module
Detects potential business risks using rule-based logic
"""

import pandas as pd
import numpy as np


class RiskDetector:
    """
    Detect business risks using simple rule-based logic
    """
    
    def __init__(self, data, thresholds=None):
        """
        Initialize the RiskDetector
        
        Args:
            data (pd.DataFrame): Business data with revenue, cost, and profit
            thresholds (dict): Custom thresholds for risk detection
        """
        self.data = data.copy()
        
        # Default thresholds
        self.thresholds = {
            'low_profit_margin': 10,  # % - Profit margin below this is risky
            'high_cost_ratio': 80,    # % - Cost/Revenue ratio above this is risky
            'negative_profit_days': 3, # Consecutive days with negative profit
            'revenue_drop': 20,       # % - Revenue drop compared to average
            'cost_spike': 30          # % - Cost spike compared to average
        }
        
        # Update with custom thresholds if provided
        if thresholds:
            self.thresholds.update(thresholds)
        
        self.risks = []
    
    def detect_all_risks(self):
        """
        Run all risk detection checks
        
        Returns:
            list: List of detected risks
        """
        self.risks = []
        
        # Run all risk detection methods
        self._detect_negative_profit()
        self._detect_low_profit_margin()
        self._detect_high_cost_ratio()
        self._detect_revenue_anomalies()
        self._detect_cost_anomalies()
        
        return self.risks
    
    def _detect_negative_profit(self):
        """
        Detect periods with negative profit
        """
        # Calculate profit
        self.data['profit'] = self.data['revenue'] - self.data['cost']
        
        # Find negative profit records
        negative_profit = self.data[self.data['profit'] < 0]
        
        if len(negative_profit) > 0:
            risk = {
                'type': 'negative_profit',
                'severity': 'high',
                'description': f"Found {len(negative_profit)} period(s) with negative profit",
                'affected_dates': negative_profit['date'].tolist(),
                'total_loss': negative_profit['profit'].sum()
            }
            self.risks.append(risk)
        
        # Detect consecutive negative profit days
        consecutive = self._find_consecutive_negative_profit()
        if consecutive > 0:
            risk = {
                'type': 'consecutive_negative_profit',
                'severity': 'critical',
                'description': f"Found {consecutive} consecutive period(s) with negative profit",
                'threshold': self.thresholds['negative_profit_days']
            }
            self.risks.append(risk)
    
    def _find_consecutive_negative_profit(self):
        """
        Find the maximum consecutive periods with negative profit
        
        Returns:
            int: Maximum consecutive negative profit periods
        """
        self.data['profit'] = self.data['revenue'] - self.data['cost']
        is_negative = (self.data['profit'] < 0).astype(int)
        
        # Find consecutive sequences
        consecutive = 0
        max_consecutive = 0
        
        for val in is_negative:
            if val == 1:
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0
        
        return max_consecutive
    
    def _detect_low_profit_margin(self):
        """
        Detect periods with low profit margin
        """
        # Calculate profit margin
        self.data['profit'] = self.data['revenue'] - self.data['cost']
        profit_margin = np.where(
            self.data['revenue'] != 0,
            (self.data['profit'] / self.data['revenue']) * 100,
            0
        )
        
        low_margin = profit_margin < self.thresholds['low_profit_margin']
        low_margin_count = np.sum(low_margin)
        
        if low_margin_count > 0:
            risk = {
                'type': 'low_profit_margin',
                'severity': 'medium',
                'description': f"Found {low_margin_count} period(s) with profit margin below {self.thresholds['low_profit_margin']}%",
                'threshold': self.thresholds['low_profit_margin'],
                'avg_margin': np.mean(profit_margin[low_margin])
            }
            self.risks.append(risk)
    
    def _detect_high_cost_ratio(self):
        """
        Detect periods with high cost-to-revenue ratio
        """
        cost_ratio = np.where(
            self.data['revenue'] != 0,
            (self.data['cost'] / self.data['revenue']) * 100,
            100
        )
        
        high_cost = cost_ratio > self.thresholds['high_cost_ratio']
        high_cost_count = np.sum(high_cost)
        
        if high_cost_count > 0:
            risk = {
                'type': 'high_cost_ratio',
                'severity': 'medium',
                'description': f"Found {high_cost_count} period(s) with cost ratio above {self.thresholds['high_cost_ratio']}%",
                'threshold': self.thresholds['high_cost_ratio'],
                'avg_ratio': np.mean(cost_ratio[high_cost])
            }
            self.risks.append(risk)
    
    def _detect_revenue_anomalies(self):
        """
        Detect unusual drops in revenue
        """
        avg_revenue = self.data['revenue'].mean()
        
        # Find significant drops
        revenue_drop = ((avg_revenue - self.data['revenue']) / avg_revenue) * 100
        significant_drops = revenue_drop > self.thresholds['revenue_drop']
        
        if np.sum(significant_drops) > 0:
            risk = {
                'type': 'revenue_drop',
                'severity': 'high',
                'description': f"Found {np.sum(significant_drops)} period(s) with revenue drop > {self.thresholds['revenue_drop']}%",
                'threshold': self.thresholds['revenue_drop'],
                'avg_revenue': avg_revenue
            }
            self.risks.append(risk)
    
    def _detect_cost_anomalies(self):
        """
        Detect unusual spikes in cost
        """
        avg_cost = self.data['cost'].mean()
        
        # Find significant spikes
        cost_spike = ((self.data['cost'] - avg_cost) / avg_cost) * 100
        significant_spikes = cost_spike > self.thresholds['cost_spike']
        
        if np.sum(significant_spikes) > 0:
            risk = {
                'type': 'cost_spike',
                'severity': 'medium',
                'description': f"Found {np.sum(significant_spikes)} period(s) with cost spike > {self.thresholds['cost_spike']}%",
                'threshold': self.thresholds['cost_spike'],
                'avg_cost': avg_cost
            }
            self.risks.append(risk)
    
    def get_risk_summary(self):
        """
        Get a summary of detected risks
        
        Returns:
            dict: Risk summary with counts by severity
        """
        if not self.risks:
            return {'total_risks': 0, 'message': 'No risks detected'}
        
        severity_counts = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for risk in self.risks:
            severity = risk.get('severity', 'low')
            severity_counts[severity] += 1
        
        return {
            'total_risks': len(self.risks),
            'by_severity': severity_counts,
            'risks': self.risks
        }
