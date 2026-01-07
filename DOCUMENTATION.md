# BizSight Decision Intelligence System - Technical Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Module Details](#module-details)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Testing](#testing)
8. [Extending the System](#extending-the-system)

## Overview

BizSight is a modular Python-based business decision intelligence system designed for analyzing structured business data. It provides comprehensive insights through data analytics, risk detection, visualization, and scenario simulation using simple rule-based logic.

### Key Features
- **Modular Design**: Clean separation of concerns with independent modules
- **Rule-Based Logic**: No ML/AI - uses simple statistical and threshold-based rules
- **Comprehensive Analytics**: Revenue, cost, profit analysis with trend detection
- **Risk Detection**: Identifies potential business risks automatically
- **Rich Visualizations**: Multiple chart types using Matplotlib
- **What-If Analysis**: Simulate various business scenarios

### Technology Stack
- Python 3.8+
- Pandas 2.0.0+ (Data manipulation)
- NumPy 1.24.0+ (Numerical operations)
- Matplotlib 3.7.0+ (Visualization)

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Main Application                      │
│                         (main.py)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
    ┌─────────────┐         ┌─────────────┐
    │ Data Loader │         │  Visualizer │
    └──────┬──────┘         └─────────────┘
           │
           ▼
    ┌─────────────────────────────────────┐
    │          Business Data              │
    └──┬─────────────┬─────────────┬──────┘
       ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Analytics  │ │Risk Detector│ │  Simulator  │
└─────────────┘ └─────────────┘ └─────────────┘
```

### Data Flow
1. **Data Loading**: CSV files are loaded and validated
2. **Analytics**: Data is analyzed for patterns, trends, and statistics
3. **Risk Detection**: Rule-based checks identify potential issues
4. **Visualization**: Results are plotted and saved
5. **Simulation**: What-if scenarios are tested

## Module Details

### 1. Data Loader (`src/data_loader.py`)

**Purpose**: Handle CSV data loading and validation

**Key Classes**:
- `DataLoader`: Main class for data operations

**Key Methods**:
- `load_data()`: Load and validate CSV file
- `get_data_summary()`: Return data statistics

**Requirements**:
- CSV must have columns: `date`, `revenue`, `cost`
- Date column is converted to datetime format
- Data is sorted by date

### 2. Business Analytics (`src/analytics.py`)

**Purpose**: Perform statistical analysis on business data

**Key Classes**:
- `BusinessAnalytics`: Main analytics engine

**Key Methods**:
- `get_summary_statistics()`: Mean, median, std, min, max
- `calculate_profit_margin()`: Profit as % of revenue
- `analyze_trends(window=3)`: Moving average trend analysis
- `get_monthly_aggregates()`: Monthly summaries
- `get_top_performing_periods()`: Best performing dates

**Calculations**:
- Profit = Revenue - Cost
- Profit Margin = (Profit / Revenue) × 100
- Trend Direction: Based on 5% threshold change

### 3. Risk Detector (`src/risk_detector.py`)

**Purpose**: Identify business risks using rule-based logic

**Key Classes**:
- `RiskDetector`: Risk detection engine

**Default Thresholds**:
- Low profit margin: < 10%
- High cost ratio: > 80%
- Negative profit days: 3 consecutive
- Revenue drop: > 20% below average
- Cost spike: > 30% above average

**Risk Severity Levels**:
- Critical: Immediate action required
- High: Significant concern
- Medium: Should be monitored
- Low: Minor issue

**Key Methods**:
- `detect_all_risks()`: Run all risk checks
- `get_risk_summary()`: Get risk statistics

### 4. Visualizer (`src/visualizer.py`)

**Purpose**: Create business intelligence visualizations

**Key Classes**:
- `Visualizer`: Visualization engine

**Supported Visualizations**:
1. **Revenue/Cost/Profit Plot**: Time series line chart
2. **Profit Margin Plot**: Margin trends over time
3. **Trends Analysis**: Moving average trends (3 subplots)
4. **Monthly Comparison**: Bar chart comparison
5. **Risk Summary**: Pie and bar charts for risks

**Key Methods**:
- `plot_revenue_cost_profit()`: Main financial plot
- `plot_profit_margin()`: Margin analysis
- `plot_trends()`: Trend visualization
- `plot_monthly_comparison()`: Monthly bars
- `plot_risk_summary()`: Risk distribution

**Output**:
- All plots saved as PNG files (300 DPI)
- Default directory: `outputs/`
- Files are ignored by git via .gitignore

### 5. Scenario Simulator (`src/scenario_simulator.py`)

**Purpose**: Simulate what-if business scenarios

**Key Classes**:
- `ScenarioSimulator`: Simulation engine

**Simulation Types**:
1. **Revenue Change**: Adjust revenue by percentage
2. **Cost Change**: Adjust cost by percentage
3. **Combined Change**: Adjust both simultaneously

**Key Methods**:
- `simulate_revenue_change(pct)`: Revenue scenario
- `simulate_cost_change(pct)`: Cost scenario
- `simulate_combined_change(rev_pct, cost_pct)`: Combined
- `compare_scenarios()`: Comparison table
- `get_best_scenario(metric)`: Find optimal scenario

**Output**:
- Original vs Simulated metrics
- Impact analysis (absolute and percentage changes)
- Comparison dataframe

## Installation & Setup

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# pip package manager
pip --version
```

### Installation Steps

1. **Clone the repository**:
```bash
git clone https://github.com/GeeteshVaity/BizSight-Decision-Intelligence.git
cd BizSight-Decision-Intelligence
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python -c "import pandas, numpy, matplotlib; print('✅ All dependencies installed')"
```

## Usage Guide

### Quick Start

Run the complete analysis:
```bash
python main.py
```

This will:
1. Load data from `data/business_data.csv`
2. Perform comprehensive analytics
3. Detect risks
4. Generate visualizations in `outputs/`
5. Simulate scenarios
6. Display summary report

### Individual Module Usage

See `example_usage.py` for detailed examples:
```bash
python example_usage.py
```

### Custom Data Analysis

```python
from src.data_loader import DataLoader
from src.analytics import BusinessAnalytics

# Load your data
loader = DataLoader('path/to/your/data.csv')
data = loader.load_data()

# Analyze
analytics = BusinessAnalytics(data)
summary = analytics.get_summary_statistics()
print(summary)
```

### Custom Risk Thresholds

```python
from src.risk_detector import RiskDetector

# Define custom thresholds
custom_thresholds = {
    'low_profit_margin': 15,  # 15% instead of default 10%
    'high_cost_ratio': 70,    # 70% instead of default 80%
}

detector = RiskDetector(data, thresholds=custom_thresholds)
risks = detector.detect_all_risks()
```

## API Reference

### DataLoader

```python
class DataLoader(filepath)
```

**Parameters**:
- `filepath` (str): Path to CSV file

**Methods**:
```python
load_data() -> pd.DataFrame
    Load and validate data from CSV

get_data_summary() -> dict
    Return summary statistics
```

### BusinessAnalytics

```python
class BusinessAnalytics(data)
```

**Parameters**:
- `data` (pd.DataFrame): Business data with date, revenue, cost

**Methods**:
```python
get_summary_statistics() -> dict
    Return statistical summary

calculate_profit_margin() -> pd.Series
    Calculate profit margins

analyze_trends(window=3) -> dict
    Analyze trends with moving average

get_monthly_aggregates() -> pd.DataFrame
    Get monthly aggregated data

get_top_performing_periods(metric='profit', top_n=5) -> pd.DataFrame
    Get top performing periods
```

### RiskDetector

```python
class RiskDetector(data, thresholds=None)
```

**Parameters**:
- `data` (pd.DataFrame): Business data
- `thresholds` (dict): Custom risk thresholds

**Methods**:
```python
detect_all_risks() -> list
    Run all risk detection checks

get_risk_summary() -> dict
    Get risk summary with counts
```

### Visualizer

```python
class Visualizer(output_dir='outputs')
```

**Parameters**:
- `output_dir` (str): Directory for saving plots

**Methods**:
```python
plot_revenue_cost_profit(data, save=True, show=False) -> str
    Plot revenue, cost, profit over time

plot_profit_margin(data, save=True, show=False) -> str
    Plot profit margin trends

plot_trends(data, trends, save=True, show=False) -> str
    Plot trend analysis

plot_monthly_comparison(monthly_data, save=True, show=False) -> str
    Plot monthly comparison bars

plot_risk_summary(risk_summary, save=True, show=False) -> str
    Plot risk distribution
```

### ScenarioSimulator

```python
class ScenarioSimulator(data)
```

**Parameters**:
- `data` (pd.DataFrame): Original business data

**Methods**:
```python
simulate_revenue_change(percentage_change, scenario_name=None) -> dict
    Simulate revenue change

simulate_cost_change(percentage_change, scenario_name=None) -> dict
    Simulate cost change

simulate_combined_change(revenue_change, cost_change, scenario_name=None) -> dict
    Simulate combined changes

compare_scenarios() -> pd.DataFrame
    Compare all scenarios

get_best_scenario(metric='profit') -> dict
    Get best scenario by metric
```

## Testing

### Run All Tests

```bash
python tests/test_bizsight.py
```

### Test Coverage

The test suite includes 14 test cases covering:
- Data loading and validation
- Analytics calculations
- Profit margin computations
- Trend analysis
- Risk detection
- Scenario simulations
- Comparison functions

### Adding New Tests

Add test cases to `tests/test_bizsight.py`:

```python
class TestNewFeature(unittest.TestCase):
    def test_new_functionality(self):
        # Your test here
        self.assertEqual(expected, actual)
```

## Extending the System

### Adding New Risk Types

Edit `src/risk_detector.py`:

```python
def _detect_custom_risk(self):
    """Detect custom risk"""
    # Your logic here
    if condition:
        risk = {
            'type': 'custom_risk',
            'severity': 'medium',
            'description': 'Custom risk detected'
        }
        self.risks.append(risk)

# Add to detect_all_risks()
def detect_all_risks(self):
    self.risks = []
    # ... existing checks
    self._detect_custom_risk()  # Add this
    return self.risks
```

### Adding New Visualizations

Edit `src/visualizer.py`:

```python
def plot_custom_chart(self, data, save=True, show=False):
    """Create custom visualization"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Your plotting code
    ax.plot(data['date'], data['value'])
    
    # Save
    if save:
        filepath = os.path.join(self.output_dir, 'custom_chart.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return filepath
```

### Adding New Scenario Types

Edit `src/scenario_simulator.py`:

```python
def simulate_custom_scenario(self, parameters):
    """Simulate custom scenario"""
    simulated_data = self.original_data.copy()
    
    # Apply your transformations
    simulated_data['revenue'] = simulated_data['revenue'] * parameters['factor']
    simulated_data['profit'] = simulated_data['revenue'] - simulated_data['cost']
    
    # Calculate impact
    scenario_result = self._calculate_scenario_impact(
        self.original_data,
        simulated_data,
        'Custom Scenario',
        'custom'
    )
    
    self.scenarios.append(scenario_result)
    return scenario_result
```

## Best Practices

1. **Data Quality**: Ensure CSV data is clean and complete
2. **Thresholds**: Adjust risk thresholds based on your business context
3. **Regular Analysis**: Run analysis regularly to track trends
4. **Scenario Planning**: Test multiple scenarios before decisions
5. **Documentation**: Keep track of insights and decisions

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError` when loading data
- **Solution**: Ensure CSV file exists at specified path

**Issue**: `ValueError: Missing required columns`
- **Solution**: Verify CSV has 'date', 'revenue', 'cost' columns

**Issue**: Plots not displaying
- **Solution**: Set `show=True` or check `outputs/` directory

**Issue**: Memory error with large datasets
- **Solution**: Process data in chunks or increase system memory

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check documentation
- Review example_usage.py for code samples

---

**Last Updated**: January 2024
**Version**: 1.0.0
