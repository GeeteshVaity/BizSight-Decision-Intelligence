"""
BizSight Decision Intelligence System
Main entry point for the business decision intelligence system
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


def print_separator(title=""):
    """Print a visual separator"""
    print("\n" + "=" * 80)
    if title:
        print(f" {title}")
        print("=" * 80)


def print_summary_statistics(summary):
    """Print summary statistics in a readable format"""
    print("\n📊 Summary Statistics:")
    
    for metric, stats in summary.items():
        print(f"\n{metric.upper()}:")
        print(f"  Total:  ${stats['total']:,.2f}")
        print(f"  Mean:   ${stats['mean']:,.2f}")
        print(f"  Median: ${stats['median']:,.2f}")
        print(f"  Std:    ${stats['std']:,.2f}")
        print(f"  Min:    ${stats['min']:,.2f}")
        print(f"  Max:    ${stats['max']:,.2f}")


def print_trends(trends):
    """Print trend analysis results"""
    print("\n📈 Trend Analysis:")
    print(f"  Revenue Trend: {trends['revenue_direction'].upper()}")
    print(f"  Cost Trend:    {trends['cost_direction'].upper()}")
    print(f"  Profit Trend:  {trends['profit_direction'].upper()}")


def print_risk_summary(risk_summary):
    """Print risk detection results"""
    print("\n⚠️  Risk Detection Results:")
    
    if risk_summary.get('total_risks', 0) == 0:
        print("  ✅ No risks detected - Business is healthy!")
        return
    
    print(f"  Total Risks Detected: {risk_summary['total_risks']}")
    print(f"\n  By Severity:")
    for severity, count in risk_summary['by_severity'].items():
        if count > 0:
            print(f"    {severity.capitalize()}: {count}")
    
    print("\n  Detailed Risks:")
    for i, risk in enumerate(risk_summary['risks'], 1):
        print(f"\n  {i}. {risk['type'].upper()} - Severity: {risk['severity'].upper()}")
        print(f"     {risk['description']}")


def print_scenario_comparison(comparison_df):
    """Print scenario comparison table"""
    print("\n🔮 Scenario Comparison:")
    print(comparison_df.to_string(index=False, float_format=lambda x: f'${x:,.2f}' if x > 1000 else f'{x:.2f}'))


def main():
    """Main function to run the Business Decision Intelligence System"""
    
    print_separator("🎯 BizSight Decision Intelligence System")
    print("\nWelcome to BizSight - Your Business Intelligence Companion")
    
    # Step 1: Load Data
    print_separator("Step 1: Loading Business Data")
    
    data_file = 'data/business_data.csv'
    if not os.path.exists(data_file):
        print(f"❌ Error: Data file not found at {data_file}")
        print("Please ensure business_data.csv exists in the data/ directory")
        return
    
    loader = DataLoader(data_file)
    data = loader.load_data()
    
    summary_info = loader.get_data_summary()
    print(f"\nData Summary:")
    print(f"  Total Records: {summary_info['total_records']}")
    print(f"  Date Range: {summary_info['date_range'][0]} to {summary_info['date_range'][1]}")
    print(f"  Columns: {', '.join(summary_info['columns'])}")
    
    # Step 2: Business Analytics
    print_separator("Step 2: Analyzing Business Metrics")
    
    analytics = BusinessAnalytics(data)
    
    # Get summary statistics
    summary_stats = analytics.get_summary_statistics()
    print_summary_statistics(summary_stats)
    
    # Analyze trends
    trends = analytics.analyze_trends(window=3)
    print_trends(trends)
    
    # Get top performing periods
    print("\n🏆 Top 5 Performing Periods (by Profit):")
    top_periods = analytics.get_top_performing_periods(metric='profit', top_n=5)
    print(top_periods.to_string(index=False))
    
    # Step 3: Risk Detection
    print_separator("Step 3: Detecting Business Risks")
    
    risk_detector = RiskDetector(data)
    risk_detector.detect_all_risks()
    risk_summary = risk_detector.get_risk_summary()
    print_risk_summary(risk_summary)
    
    # Step 4: Visualizations
    print_separator("Step 4: Creating Visualizations")
    
    visualizer = Visualizer(output_dir='outputs')
    
    # Create various plots
    print("\nGenerating visualizations...")
    visualizer.plot_revenue_cost_profit(data, save=True, show=False)
    visualizer.plot_profit_margin(data, save=True, show=False)
    visualizer.plot_trends(data, trends, save=True, show=False)
    
    # Monthly comparison
    monthly_data = analytics.get_monthly_aggregates()
    visualizer.plot_monthly_comparison(monthly_data, save=True, show=False)
    
    # Risk visualization
    if risk_summary.get('total_risks', 0) > 0:
        visualizer.plot_risk_summary(risk_summary, save=True, show=False)
    
    print("✅ All visualizations saved to 'outputs/' directory")
    
    # Step 5: Scenario Simulation
    print_separator("Step 5: What-If Scenario Analysis")
    
    simulator = ScenarioSimulator(data)
    
    print("\nRunning scenario simulations...")
    
    # Scenario 1: Revenue increase
    scenario1 = simulator.simulate_revenue_change(10, "Optimistic: +10% Revenue")
    print(f"\n✅ Scenario 1: {scenario1['scenario_name']}")
    print(f"   Profit Change: ${scenario1['impact']['profit_change']:,.2f} ({scenario1['impact']['profit_pct_change']:.2f}%)")
    
    # Scenario 2: Revenue decrease
    scenario2 = simulator.simulate_revenue_change(-10, "Pessimistic: -10% Revenue")
    print(f"\n✅ Scenario 2: {scenario2['scenario_name']}")
    print(f"   Profit Change: ${scenario2['impact']['profit_change']:,.2f} ({scenario2['impact']['profit_pct_change']:.2f}%)")
    
    # Scenario 3: Cost reduction
    scenario3 = simulator.simulate_cost_change(-15, "Efficiency: -15% Cost")
    print(f"\n✅ Scenario 3: {scenario3['scenario_name']}")
    print(f"   Profit Change: ${scenario3['impact']['profit_change']:,.2f} ({scenario3['impact']['profit_pct_change']:.2f}%)")
    
    # Scenario 4: Combined change
    scenario4 = simulator.simulate_combined_change(5, -10, "Balanced: +5% Revenue, -10% Cost")
    print(f"\n✅ Scenario 4: {scenario4['scenario_name']}")
    print(f"   Profit Change: ${scenario4['impact']['profit_change']:,.2f} ({scenario4['impact']['profit_pct_change']:.2f}%)")
    
    # Compare all scenarios
    comparison = simulator.compare_scenarios()
    print_scenario_comparison(comparison)
    
    # Get best scenario
    best_scenario = simulator.get_best_scenario(metric='profit')
    print(f"\n🌟 Best Scenario (by Total Profit): {best_scenario['scenario_name']}")
    print(f"   Total Profit: ${best_scenario['simulated']['total_profit']:,.2f}")
    print(f"   Profit Margin: {best_scenario['simulated']['profit_margin']:.2f}%")
    
    # Final Summary
    print_separator("Summary & Recommendations")
    
    print("\n📋 Key Insights:")
    print(f"  • Total Revenue: ${summary_stats['revenue']['total']:,.2f}")
    print(f"  • Total Costs: ${summary_stats['cost']['total']:,.2f}")
    print(f"  • Total Profit: ${summary_stats['profit']['total']:,.2f}")
    print(f"  • Overall Trend: Revenue is {trends['revenue_direction']}, Profit is {trends['profit_direction']}")
    
    if risk_summary.get('total_risks', 0) > 0:
        print(f"  • ⚠️  {risk_summary['total_risks']} risk(s) detected - Review required!")
    else:
        print("  • ✅ No significant risks detected")
    
    print(f"\n💡 Recommendation: Consider the '{best_scenario['scenario_name']}' strategy")
    print(f"   Expected profit improvement: ${best_scenario['impact']['profit_change']:,.2f}")
    
    print_separator("Analysis Complete")
    print("\n✨ Thank you for using BizSight Decision Intelligence System!")
    print("📁 All reports and visualizations are saved in the 'outputs/' directory\n")


if __name__ == "__main__":
    main()
