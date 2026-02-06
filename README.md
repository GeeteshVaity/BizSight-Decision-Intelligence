# BizSight – AI-Assisted Business Decision Intelligence

**BizSight** is a sophisticated Python-based decision intelligence system designed to transform raw business data into actionable strategic insights. By combining rigorous rule-based financial logic with AI-powered natural language explanations, BizSight helps small-to-medium enterprises (SMEs) identify risks, simulate market changes, and generate professional business reports without the complexity of traditional BI tools.

---

## Key Features

* **Automated Data Processing**: Load and validate CSV-based transactional data, automatically calculating revenue, cost, profit, and margins.
* **Intelligent Risk Detection**: Rule-based monitoring for declining revenue trends, continuous losses, and high cost-to-revenue ratios.
* **Interactive "What-If" Simulations**: Predict the impact of revenue or cost changes on your bottom line with side-by-side comparisons.
* **Explainable AI (XAI)**: Uses AI strictly for generating human-readable summaries and strategic recommendations, ensuring all financial calculations remain transparent and logic-driven.
* **Professional Reporting**: Generate comprehensive text-based summaries and downloadable PDF reports featuring embedded data visualizations.

---

## Technology Stack

| Layer | Technology |
| --- | --- |
| **Core Logic** | Python, Pandas, NumPy |
| **Interface** | Streamlit (Web Dashboard) |
| **Visualization** | Plotly, Matplotlib |
| **AI Engine** | Groq API (Natural Language Explanations) |
| **Reporting** | ReportLab (PDF Generation) |

---

## Project Structure

```text
BizSight/
├── app.py                  # Streamlit Web Dashboard
├── core/                   # Data loading, mapping, and validation
├── analysis/               # Financial calculations and trend analysis
├── intelligence/           # Risk detection and AI insight generation
├── simulation/             # "What-if" scenario and comparison logic
├── visualization/          # Interactive chart generation
├── reports/                # Text and PDF report generation engines
├── data/                   # Sample datasets
└── main.py                 # CLI pipeline version

```

---

## Getting Started

### 1. Prerequisites

Ensure you have Python installed. You will also need a **Groq API Key** configured in your environment to enable AI insights.

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd BizSight

# Install required dependencies
pip install -r requirements.txt

```

### 3. Launch the Dashboard

```bash
streamlit run app.py

```

---

## Dashboard Workflow

1. **Upload**: Provide a CSV with columns: `date`, `product_name`, `quantity`, `selling_price`, `revenue`, and `cost`.
2. **Analyze**: View real-time metrics for total performance and margin health.
3. **Audit**: Review automated risk alerts (e.g., "Continuous Loss Detected").
4. **Simulate**: Use sliders to adjust revenue/cost percentages and see immediate profit impact.
5. **Report**: Generate AI-powered insights and download the full PDF report for stakeholders.

---

## 👥 The Team

| Member | Responsibility |
| --- | --- |
| **Geetesh** | Project Lead, GUI Integration, AI Integration |
| **Dhruv** | Business Logic, Risk Detection, Insights |
| **Jay** | Visualization, Simulation, Report Generation |

---

## 🎓 Academic Justification

BizSight was built to demonstrate **modular software architecture**, **explainable AI implementation**, and **rule-based expert systems** in a collaborative environment using Git/GitHub.
