# 📊 BizSight – AI-Assisted Business Decision Intelligence System

BizSight is a **Python-based business decision intelligence system** that helps users analyze business data, detect risks, visualize trends, simulate decisions, and generate meaningful insights using **rule-based logic combined with AI-powered explanations**.

The system is designed to be:

* Explainable
* Modular
* Practical
* Examiner-friendly
> BizSight focuses on **decision support**, not prediction.
> All calculations are done using Python logic, while AI is used only for explanation and reporting.

---

## 🚀 Project Motivation & Idea

Small businesses often rely on spreadsheets for data analysis, which:

* Are error-prone
* Do not highlight risks automatically
* Do not explain insights clearly
* Do not support decision simulation

**BizSight solves this problem** by acting as a smart decision-support tool that:

* Analyzes CSV-based business data
* Detects financial risks using predefined rules
* Visualizes trends for easy understanding
* Simulates “what-if” business scenarios
* Uses AI to convert numbers into human-readable insights

---

## 🧠 What This Project Does (In Simple Words)

BizSight allows a user to:

1. Upload business data (CSV file)
2. Automatically calculate revenue, cost, profit, and margins
3. Analyze product-wise and time-wise performance
4. Detect risks like losses or declining trends
5. Visualize data using charts
6. Simulate changes in revenue or cost
7. Compare original vs simulated outcomes
8. Generate AI-assisted insights and reports
9. Interact with everything using a GUI dashboard

---

## 🛠️ Technologies Used

| Layer                | Technology                |
| -------------------- | ------------------------- |
| Programming Language | Python                    |
| Data Handling        | Pandas, NumPy             |
| Visualization        | Matplotlib / Plotly       |
| GUI                  | Streamlit                 |
| AI Integration       | AI API (Explanation only) |
| Version Control      | Git + GitHub              |

⚠️ **Important Note**

* No machine learning models are used
* No predictions or training
* AI is used strictly for **explanation and report generation**

---

## 📁 Project Folder Structure

```
BizSight/
│
├── app/
│   └── app.py                  # Streamlit GUI
│
├── core/
│   ├── data_loader.py          # CSV loading
│   └── data_validator.py       # Data validation & cleaning
│
├── analysis/
│   ├── analyzer.py             # Business calculations
│   └── trends.py               # Time-based analysis
│
├── intelligence/
│   ├── risk_detector.py        # Rule-based risk detection
│   └── insight_generator.py    # Text insights (logic-based)
│
├── simulation/
│   ├── simulator.py            # What-if scenarios
│   └── comparator.py           # Comparison logic
│
├── visualization/
│   └── charts.py               # Graph generation
│
├── ai/
│   ├── ai_client.py            # AI API integration
│   ├── prompt_builder.py       # Safe AI prompts
│   └── ai_insights.py          # AI-generated explanations
│
├── reports/
│   └── report_generator.py     # Final report creation
│
├── data/
│   └── sample_data.csv
│
├── main.py                     # CLI backup version
├── requirements.txt
└── README.md
```

---

## 👥 Team & Responsibilities

| Member      | Responsibility                                |
| ----------- | --------------------------------------------- |
| **Geetesh** | Project Lead, GUI integration, AI integration |
| **Dhruv**   | Business logic, risk detection, insights      |
| **Jay**     | Visualization, simulation, report generation  |

The project is developed using **branch-based collaboration** on GitHub.

---

## 🔄 Development Workflow (How We Built It)

1. Repository created with modular folder structure
2. CSV data loading and validation implemented
3. Core business calculations developed
4. Trend and product analysis added
5. Rule-based risk detection implemented
6. Visualization modules created
7. What-if simulation logic added
8. AI layer integrated for explanation only
9. Streamlit GUI built to connect everything
10. Final testing and integration completed

---

## 🧪 How to Set Up the Project (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd BizSight
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application (GUI)

```bash
streamlit run app/app.py
```

### 5️⃣ (Optional) Run CLI Version

```bash
python main.py
```

---

## 🖥️ How to Use the BizSight Application

### Step 1: Upload Data

* Upload a CSV file containing:

  * Date
  * Product
  * Revenue
  * Cost
  * Quantity

### Step 2: Data Processing

* The system automatically:

  * Validates data
  * Cleans missing values
  * Creates derived metrics like profit and margin

### Step 3: Business Analysis

* View:

  * Total revenue
  * Total cost
  * Total profit
  * Profit margin
* Analyze product-wise and time-wise performance

### Step 4: Risk Detection

* The system flags:

  * Loss-making products
  * Declining revenue trends
  * High cost-to-revenue ratios

### Step 5: Visualization

* Interactive charts:

  * Revenue over time
  * Profit per product
  * Revenue contribution

### Step 6: What-If Simulation

* Adjust revenue or cost percentages
* See impact on profit
* Compare original vs simulated results

### Step 7: AI Insights & Report

* AI explains:

  * Business performance
  * Detected risks
  * Simulation impact
* Generate a downloadable business report

---

## 🤖 How AI Is Used (Very Important)

AI is used **only after** all calculations are completed.

### AI Responsibilities

* Convert numeric results into explanations
* Summarize risks in natural language
* Generate readable business reports

### AI Restrictions

* AI does NOT calculate values
* AI does NOT predict future outcomes
* AI does NOT learn from data

This ensures transparency and exam safety.

---

## 📄 Output & Results

BizSight provides:

* Clean numerical metrics
* Visual dashboards
* Risk alerts
* Decision insights
* Scenario comparison results
* Text-based business report

---

## 🎓 Academic & Viva Justification

This project demonstrates:

* Modular software architecture
* Data analysis using Python
* Rule-based decision systems
* Ethical and explainable AI usage
* GUI-based application design
* Version-controlled collaborative development

---

## 🧠 Final Project Summary

**BizSight** is a practical, AI-assisted decision intelligence system that helps users understand business performance, detect financial risks, visualize trends, and evaluate decisions using Python-based analytics and a user-friendly interface.

---

## ✅ Future Enhancements (Optional)

* Role-based access
* Database integration
* Advanced dashboards
* Export reports as PDF

---

## 🏁 Final Note

This project is designed to be:

* Easy to explain
* Easy to demonstrate
* Easy to defend in exams

If something works in BizSight, it works **because of logic first, AI second**.

---

**— Team BizSight 🚀**
