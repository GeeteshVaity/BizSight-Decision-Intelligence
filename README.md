# BizSight Decision Intelligence System 🎯

BizSight is a modular Python-based business decision intelligence system that analyzes structured business data to generate insights, detect risks, and simulate what-if scenarios using rule-based logic and data visualization.

## 🌟 Features

- **📊 Data Loading**: Load business data from CSV files with automatic validation
- **📈 Business Analytics**: Analyze revenue, cost, profit, and trends
- **⚠️ Risk Detection**: Detect potential risks using simple rule-based logic
- **📉 Visualizations**: Create insightful charts and graphs with Matplotlib
- **🔮 Scenario Simulation**: Simulate what-if scenarios by adjusting revenue or cost parameters

## 📁 Project Structure

```
BizSight-Decision-Intelligence/
│
├── data/                      # Data directory
│   └── business_data.csv      # Sample business data
│
├── src/                       # Source code modules
│   ├── __init__.py           # Package initialization
│   ├── data_loader.py        # Data loading and validation
│   ├── analytics.py          # Business analytics module
│   ├── risk_detector.py      # Risk detection module
│   ├── visualizer.py         # Visualization module
│   └── scenario_simulator.py # Scenario simulation module
│
├── outputs/                   # Output directory for visualizations
│
├── tests/                     # Unit tests (if applicable)
│
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── LICENSE                    # License file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/GeeteshVaity/BizSight-Decision-Intelligence.git
cd BizSight-Decision-Intelligence
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Usage

Run the main script to analyze the sample business data:

```bash
python main.py
```

The system will:
1. Load business data from `data/business_data.csv`
2. Perform comprehensive business analytics
3. Detect potential risks
4. Generate visualizations in the `outputs/` directory
5. Simulate various what-if scenarios
6. Display a detailed summary and recommendations

## 📊 Module Details

### 1. Data Loader (`data_loader.py`)

Handles loading and validating business data from CSV files.

**Key Features:**
- Loads CSV files with date, revenue, and cost columns
- Validates data integrity
- Provides data summary statistics

**Usage Example:**
```python
from src.data_loader import DataLoader

loader = DataLoader('data/business_data.csv')
data = loader.load_data()
summary = loader.get_data_summary()
```

### 2. Business Analytics (`analytics.py`)

Analyzes business metrics including revenue, cost, profit, and trends.

**Key Features:**
- Calculate summary statistics (mean, median, std, min, max)
- Compute profit margins
- Analyze trends using moving averages
- Generate monthly aggregates
- Identify top performing periods

**Usage Example:**
```python
from src.analytics import BusinessAnalytics

analytics = BusinessAnalytics(data)
summary = analytics.get_summary_statistics()
trends = analytics.analyze_trends(window=3)
monthly_data = analytics.get_monthly_aggregates()
```

### 3. Risk Detector (`risk_detector.py`)

Detects potential business risks using rule-based logic.

**Risk Types Detected:**
- Negative profit periods
- Low profit margins
- High cost-to-revenue ratios
- Revenue drops
- Cost spikes

**Usage Example:**
```python
from src.risk_detector import RiskDetector

risk_detector = RiskDetector(data)
risk_detector.detect_all_risks()
risk_summary = risk_detector.get_risk_summary()
```

### 4. Visualizer (`visualizer.py`)

Creates various visualizations for business intelligence.

**Visualizations:**
- Revenue, cost, and profit over time
- Profit margin trends
- Trend analysis with moving averages
- Monthly comparisons
- Risk summaries

**Usage Example:**
```python
from src.visualizer import Visualizer

visualizer = Visualizer(output_dir='outputs')
visualizer.plot_revenue_cost_profit(data)
visualizer.plot_profit_margin(data)
visualizer.plot_trends(data, trends)
```

### 5. Scenario Simulator (`scenario_simulator.py`)

Simulates what-if scenarios by adjusting business parameters.

**Scenario Types:**
- Revenue change simulations
- Cost change simulations
- Combined revenue and cost changes

**Usage Example:**
```python
from src.scenario_simulator import ScenarioSimulator

simulator = ScenarioSimulator(data)
scenario1 = simulator.simulate_revenue_change(10)  # +10% revenue
scenario2 = simulator.simulate_cost_change(-15)     # -15% cost
comparison = simulator.compare_scenarios()
best = simulator.get_best_scenario(metric='profit')
```

## 📋 Data Format

The system expects CSV files with the following columns:

| Column   | Type     | Description                    |
|----------|----------|--------------------------------|
| date     | Date     | Date of the business record    |
| revenue  | Numeric  | Revenue amount for the period  |
| cost     | Numeric  | Cost amount for the period     |

**Example:**
```csv
date,revenue,cost
2024-01-01,15000,11000
2024-01-02,16500,10500
2024-01-03,14800,11200
```

## 🎨 Output Visualizations

The system generates the following visualizations in the `outputs/` directory:

1. **revenue_cost_profit.png** - Time series plot of revenue, cost, and profit
2. **profit_margin.png** - Profit margin trends over time
3. **trends_analysis.png** - Trend analysis with moving averages
4. **monthly_comparison.png** - Monthly comparison bar charts
5. **risk_summary.png** - Risk distribution visualizations (if risks detected)

## 🛠️ Technologies Used

- **Python 3.8+** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Matplotlib** - Data visualization

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Geetesh Vaity**

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📞 Support

For support or questions, please open an issue in the GitHub repository.

---

**Note:** This is a college project focused on demonstrating modular Python programming, data analysis, and visualization concepts. It uses simple rule-based logic and does not include machine learning or AI predictions.
