# Sales Forecasting for Businesses

## 📊 Project Overview

This project analyzes historical business sales data and uses
Python, SQL, and Power BI to identify sales trends, profitability
patterns, regional performance, discount impact, and future sales
forecasts.

The project follows a complete data analytics workflow:

Raw Data → Cleaning → EDA → SQL → Time Series Analysis
→ Forecasting → Model Evaluation → Power BI → Business Recommendations

---

## 🎯 Objectives

- Analyze historical sales and profit performance
- Clean and validate business transaction data
- Identify profitable and loss-making product categories
- Analyze regional and customer-segment performance
- Study sales seasonality and trends
- Build sales forecasting models
- Evaluate forecasting performance
- Create an interactive Power BI dashboard
- Generate actionable business recommendations

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- SQLite
- SQL
- Power BI
- Git & GitHub

---

## 📁 Project Structure

```text
Sales-Forecasting-for-Businesses/
│
├── data/
│   ├── raw/
│   │   └── Sample - Superstore.csv
│   │
│   ├── messy/
│   │   └── sales_messy.csv
│   │
│   └── processed/
│       ├── sales_cleaned.csv
│       ├── sales_messy_practice_cleaned.csv
│       ├── monthly_sales_timeseries.csv
│       ├── future_sales_forecast.csv
│       └── model_evaluation_results.csv
│
├── Power BI/
│   └── Sales-Forecasting-for-Businesses.pbix
│
├── business_recommendations.py
├── create_database.py
├── forecasting.py
├── main.py
├── model_evaluation.py
├── sql_queries.py
├── time_series.py
│
├── requirements.txt
├── README.md
└── .gitignore