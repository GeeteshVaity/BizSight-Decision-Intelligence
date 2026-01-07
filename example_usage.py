"""
Example Usage Script for BizSight Decision Intelligence System
This script demonstrates how to use individual modules
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from analytics import BusinessAnalytics
from risk_detector import RiskDetector
from visualizer import Visualizer
from scenario_simulator import ScenarioSimulator


def example_data_loading():
    """Example: Load and inspect data"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Data Loading")
    print("="*60)
    
    # Load data
    loader = DataLoader('data/business_data.csv')
    data = loader.load_data()
    
    # Get summary
    summary = loader.get_data_summary()
    print(f"\nLoaded {summary['total_records']} records")
    print(f"Date range: {summary['date_range'][0]} to {summary['date_range'][1]}")
    
    # Display first few records
    print("\nFirst 5 records:")
    print(data.head())
    
    return data


def example_analytics(data):
    """Example: Perform business analytics"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Business Analytics")
    print("="*60)
    
    # Initialize analytics
    analytics = BusinessAnalytics(data)
    
    # Get summary statistics
    summary = analytics.get_summary_statistics()
    print(f"\nTotal Revenue: ${summary['revenue']['total']:,.2f}")
    print(f"Total Cost:    ${summary['cost']['total']:,.2f}")
    print(f"Total Profit:  ${summary['profit']['total']:,.2f}")
    
    # Calculate profit margin
    profit_margins = analytics.calculate_profit_margin()
    print(f"\nAverage Profit Margin: {profit_margins.mean():.2f}%")
    
    # Analyze trends
    trends = analytics.analyze_trends(window=3)
    print(f"\nTrend Analysis:")
    print(f"  Revenue: {trends['revenue_direction']}")
    print(f"  Cost: {trends['cost_direction']}")
    print(f"  Profit: {trends['profit_direction']}")
    
    # Get monthly aggregates
    monthly = analytics.get_monthly_aggregates()
    print(f"\nMonthly Aggregates:")
    print(monthly)
    
    return analytics, trends


def example_risk_detection(data):
    """Example: Detect business risks"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Risk Detection")
    print("="*60)
    
    # Initialize risk detector with custom thresholds
    custom_thresholds = {
        'low_profit_margin': 15,  # 15% threshold
        'high_cost_ratio': 75,    # 75% threshold
    }
    
    risk_detector = RiskDetector(data, thresholds=custom_thresholds)
    risks = risk_detector.detect_all_risks()
    
    print(f"\nDetected {len(risks)} risk(s)")
    
    for i, risk in enumerate(risks, 1):
        print(f"\nRisk {i}:")
        print(f"  Type: {risk['type']}")
        print(f"  Severity: {risk['severity']}")
        print(f"  Description: {risk['description']}")
    
    # Get risk summary
    risk_summary = risk_detector.get_risk_summary()
    
    return risk_summary


def example_visualization(data, trends, risk_summary):
    """Example: Create visualizations"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Visualizations")
    print("="*60)
    
    # Initialize visualizer
    visualizer = Visualizer(output_dir='outputs/examples')
    
    print("\nGenerating visualizations...")
    
    # Create revenue/cost/profit plot
    visualizer.plot_revenue_cost_profit(data, save=True, show=False)
    print("  ✓ Revenue, Cost, Profit plot created")
    
    # Create profit margin plot
    visualizer.plot_profit_margin(data, save=True, show=False)
    print("  ✓ Profit margin plot created")
    
    # Create trends plot
    visualizer.plot_trends(data, trends, save=True, show=False)
    print("  ✓ Trends analysis plot created")
    
    # Create risk summary plot (if risks exist)
    if risk_summary.get('total_risks', 0) > 0:
        visualizer.plot_risk_summary(risk_summary, save=True, show=False)
        print("  ✓ Risk summary plot created")
    
    print("\n✅ All visualizations saved to 'outputs/examples/' directory")


def example_scenario_simulation(data):
    """Example: Simulate what-if scenarios"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Scenario Simulation")
    print("="*60)
    
    # Initialize simulator
    simulator = ScenarioSimulator(data)
    
    # Simulate revenue increase
    print("\nScenario 1: What if revenue increases by 15%?")
    scenario1 = simulator.simulate_revenue_change(15, "Revenue +15%")
    print(f"  Original Profit: ${scenario1['original']['total_profit']:,.2f}")
    print(f"  Simulated Profit: ${scenario1['simulated']['total_profit']:,.2f}")
    print(f"  Change: ${scenario1['impact']['profit_change']:,.2f} ({scenario1['impact']['profit_pct_change']:.2f}%)")
    
    # Simulate cost reduction
    print("\nScenario 2: What if costs decrease by 20%?")
    scenario2 = simulator.simulate_cost_change(-20, "Cost -20%")
    print(f"  Original Profit: ${scenario2['original']['total_profit']:,.2f}")
    print(f"  Simulated Profit: ${scenario2['simulated']['total_profit']:,.2f}")
    print(f"  Change: ${scenario2['impact']['profit_change']:,.2f} ({scenario2['impact']['profit_pct_change']:.2f}%)")
    
    # Simulate combined changes
    print("\nScenario 3: What if revenue +10% and cost -10%?")
    scenario3 = simulator.simulate_combined_change(10, -10, "Combined +10%/-10%")
    print(f"  Original Profit: ${scenario3['original']['total_profit']:,.2f}")
    print(f"  Simulated Profit: ${scenario3['simulated']['total_profit']:,.2f}")
    print(f"  Change: ${scenario3['impact']['profit_change']:,.2f} ({scenario3['impact']['profit_pct_change']:.2f}%)")
    
    # Compare scenarios
    print("\n" + "-"*60)
    print("Scenario Comparison:")
    print("-"*60)
    comparison = simulator.compare_scenarios()
    print(comparison.to_string(index=False))
    
    # Get best scenario
    best = simulator.get_best_scenario(metric='profit')
    print(f"\n🌟 Best scenario: {best['scenario_name']}")
    print(f"   Profit: ${best['simulated']['total_profit']:,.2f}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("BizSight Decision Intelligence System - Usage Examples")
    print("="*60)
    
    # Example 1: Load data
    data = example_data_loading()
    
    # Example 2: Analytics
    analytics, trends = example_analytics(data)
    
    # Example 3: Risk detection
    risk_summary = example_risk_detection(data)
    
    # Example 4: Visualizations
    example_visualization(data, trends, risk_summary)
    
    # Example 5: Scenario simulation
    example_scenario_simulation(data)
    
    print("\n" + "="*60)
    print("✨ All examples completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
