"""
Unit Tests for BizSight Decision Intelligence System
Simple tests to validate core functionality
"""

import sys
import os
import unittest
import pandas as pd
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import DataLoader
from analytics import BusinessAnalytics
from risk_detector import RiskDetector
from scenario_simulator import ScenarioSimulator


class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'business_data.csv')
    
    def test_load_data_success(self):
        """Test successful data loading"""
        loader = DataLoader(self.data_path)
        data = loader.load_data()
        
        self.assertIsNotNone(data)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn('date', data.columns)
        self.assertIn('revenue', data.columns)
        self.assertIn('cost', data.columns)
    
    def test_data_summary(self):
        """Test data summary generation"""
        loader = DataLoader(self.data_path)
        loader.load_data()
        summary = loader.get_data_summary()
        
        self.assertIn('total_records', summary)
        self.assertIn('date_range', summary)
        self.assertIn('columns', summary)


class TestBusinessAnalytics(unittest.TestCase):
    """Test cases for BusinessAnalytics"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create sample data
        self.data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'revenue': [10000, 12000, 11000, 13000, 14000, 15000, 13000, 12000, 14000, 16000],
            'cost': [7000, 8000, 7500, 8500, 9000, 9500, 8500, 8000, 9000, 10000]
        })
    
    def test_summary_statistics(self):
        """Test summary statistics calculation"""
        analytics = BusinessAnalytics(self.data)
        summary = analytics.get_summary_statistics()
        
        self.assertIn('revenue', summary)
        self.assertIn('cost', summary)
        self.assertIn('profit', summary)
        self.assertIn('total', summary['revenue'])
        self.assertIn('mean', summary['revenue'])
    
    def test_profit_calculation(self):
        """Test profit calculation"""
        analytics = BusinessAnalytics(self.data)
        
        # Check if profit column is created
        self.assertIn('profit', analytics.data.columns)
        
        # Verify profit calculation
        expected_profit = self.data['revenue'].iloc[0] - self.data['cost'].iloc[0]
        actual_profit = analytics.data['profit'].iloc[0]
        self.assertEqual(expected_profit, actual_profit)
    
    def test_profit_margin(self):
        """Test profit margin calculation"""
        analytics = BusinessAnalytics(self.data)
        margins = analytics.calculate_profit_margin()
        
        self.assertEqual(len(margins), len(self.data))
        self.assertTrue(all(margins >= 0))
    
    def test_trends(self):
        """Test trend analysis"""
        analytics = BusinessAnalytics(self.data)
        trends = analytics.analyze_trends(window=3)
        
        self.assertIn('revenue_trend', trends)
        self.assertIn('cost_trend', trends)
        self.assertIn('profit_trend', trends)
        self.assertIn('revenue_direction', trends)


class TestRiskDetector(unittest.TestCase):
    """Test cases for RiskDetector"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create data with some risks
        self.data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'revenue': [10000, 12000, 11000, 13000, 5000, 15000, 13000, 12000, 14000, 16000],
            'cost': [7000, 8000, 7500, 8500, 6000, 9500, 8500, 8000, 9000, 10000]
        })
    
    def test_detect_all_risks(self):
        """Test risk detection"""
        detector = RiskDetector(self.data)
        risks = detector.detect_all_risks()
        
        self.assertIsInstance(risks, list)
    
    def test_risk_summary(self):
        """Test risk summary generation"""
        detector = RiskDetector(self.data)
        detector.detect_all_risks()
        summary = detector.get_risk_summary()
        
        self.assertIn('total_risks', summary)
    
    def test_negative_profit_detection(self):
        """Test negative profit detection"""
        # Create data with guaranteed negative profit
        data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=5),
            'revenue': [10000, 12000, 8000, 13000, 14000],
            'cost': [11000, 11000, 12000, 10000, 11000]
        })
        
        detector = RiskDetector(data)
        risks = detector.detect_all_risks()
        
        # Should detect negative profit
        risk_types = [r['type'] for r in risks]
        self.assertIn('negative_profit', risk_types)


class TestScenarioSimulator(unittest.TestCase):
    """Test cases for ScenarioSimulator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'revenue': [10000] * 10,
            'cost': [7000] * 10
        })
    
    def test_revenue_change_simulation(self):
        """Test revenue change simulation"""
        simulator = ScenarioSimulator(self.data)
        scenario = simulator.simulate_revenue_change(10)
        
        self.assertIn('scenario_name', scenario)
        self.assertIn('original', scenario)
        self.assertIn('simulated', scenario)
        self.assertIn('impact', scenario)
        
        # Verify 10% increase
        original_revenue = scenario['original']['total_revenue']
        simulated_revenue = scenario['simulated']['total_revenue']
        expected_increase = original_revenue * 0.10
        
        self.assertAlmostEqual(simulated_revenue - original_revenue, expected_increase, places=2)
    
    def test_cost_change_simulation(self):
        """Test cost change simulation"""
        simulator = ScenarioSimulator(self.data)
        scenario = simulator.simulate_cost_change(-15)
        
        # Verify 15% decrease
        original_cost = scenario['original']['total_cost']
        simulated_cost = scenario['simulated']['total_cost']
        expected_decrease = original_cost * 0.15
        
        self.assertAlmostEqual(original_cost - simulated_cost, expected_decrease, places=2)
    
    def test_combined_simulation(self):
        """Test combined change simulation"""
        simulator = ScenarioSimulator(self.data)
        scenario = simulator.simulate_combined_change(10, -10)
        
        self.assertIn('impact', scenario)
        self.assertGreater(scenario['simulated']['total_profit'], scenario['original']['total_profit'])
    
    def test_scenario_comparison(self):
        """Test scenario comparison"""
        simulator = ScenarioSimulator(self.data)
        simulator.simulate_revenue_change(10)
        simulator.simulate_cost_change(-10)
        
        comparison = simulator.compare_scenarios()
        
        self.assertIsInstance(comparison, pd.DataFrame)
        self.assertGreater(len(comparison), 2)  # Baseline + 2 scenarios
    
    def test_best_scenario(self):
        """Test best scenario selection"""
        simulator = ScenarioSimulator(self.data)
        simulator.simulate_revenue_change(10)
        simulator.simulate_cost_change(-20)
        
        best = simulator.get_best_scenario(metric='profit')
        
        self.assertIsNotNone(best)
        self.assertIn('scenario_name', best)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestBusinessAnalytics))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestScenarioSimulator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("\n" + "="*70)
    print("BizSight Decision Intelligence System - Unit Tests")
    print("="*70 + "\n")
    
    result = run_tests()
    
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.")
    print("="*70 + "\n")
    
    sys.exit(0 if result.wasSuccessful() else 1)
