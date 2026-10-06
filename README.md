# 📈 Sales Forecasting for Businesses

An end-to-end **Data Analytics + Sales Forecasting** project built on the Superstore sales dataset. It covers data cleaning and validation, exploratory analysis, SQL analysis, time series analysis, forecasting with model evaluation, business recommendations, and two dashboards: **Power BI** and **Streamlit**.

Built as a portfolio project by a BTech IT student.

🔗 **GitHub Repository:** [shubham17-web/Sales-Forecasting-for-Businesses](https://github.com/shubham17-web/Sales-Forecasting-for-Businesses.git)
🚀 **Live Streamlit Demo:** [Open the dashboard](https://sales-forecasting-for-businesses-xwvfj9o7bje8zzgdqm75n4.streamlit.app/)

---

## 📌 Table of Contents

- [Project Goal](#-project-goal)
- [Tech Stack](#-tech-stack)
- [Dataset](#-dataset)
- [Data Cleaning & Validation](#-data-cleaning--validation)
- [Exploratory Data Analysis](#-exploratory-data-analysis)
- [SQL Analysis](#-sql-analysis)
- [Time Series Analysis](#-time-series-analysis)
- [Forecasting](#-forecasting)
- [Model Evaluation](#-model-evaluation)
- [Key Findings](#-key-findings)
- [Business Recommendations](#-business-recommendations)
- [Streamlit Dashboard](#-streamlit-dashboard)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Screenshots / Demo](#-screenshots--demo)
- [Project Structure](#-project-structure)
- [How to Run Locally](#-how-to-run-locally)

---

## 🎯 Project Goal

Build an end-to-end business analytics and sales forecasting solution that takes raw Superstore sales data through the following workflow:

```
Raw Data
  → Data Cleaning & Validation
  → Exploratory Data Analysis
  → SQL Analysis
  → Time Series Analysis
  → Sales Forecasting
  → Model Evaluation
  → Business Recommendations
  → Power BI Dashboard
  → Streamlit Dashboard
```

## 🛠 Tech Stack

| Category | Tools |
|---|---|
| Language | Python, SQL |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Modeling | Scikit-learn |
| Database | SQLite |
| Dashboards | Power BI, Streamlit |
| Version Control | Git, GitHub |

## 📂 Dataset

| Item | Details |
|---|---|
| Dataset | Sample - Superstore |
| Source | [Kaggle: Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) |
| Size | 9,994 rows × 21 columns |
| Period | 2014-01-03 to 2017-12-30 |

**Important columns include:** Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Region, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit.

> The original CSV required `latin1` encoding while loading.

## 🧹 Data Cleaning & Validation

The dataset was checked for missing values, exact duplicate rows, repeated Order IDs, invalid dates, negative sales, invalid quantities, invalid discount values, negative profit, data types, and business logic consistency.

| Check | Result |
|---|---:|
| Missing values | 0 |
| Exact duplicate rows | 0 |
| Repeated Order IDs | 4,985 |
| Invalid ship dates | 0 |
| Negative sales | 0 |
| Quantity ≤ 0 | 0 |
| Discount outside 0–1 | 0 |
| Negative profit rows | 1,871 |

**Decisions made:**

- **Repeated Order IDs were kept.** One order can contain multiple line items, so repeated IDs are expected and not duplicates.
- **Negative profit rows were kept.** They represent real business losses, not invalid data, and removing them would hide important findings.

The cleaned dataset is saved as `data/processed/sales_cleaned.csv`.

## 🔍 Exploratory Data Analysis

Main areas explored: sales and profit by category, sales and profit by region, sub-category performance, monthly sales and profit, yearly sales, discount vs profit, profit margins, and top and bottom performing products.

### By Category

| Category | Sales | Profit | Profit Margin |
|---|---:|---:|---:|
| Technology | $836,154.00 | $145,454.95 | 17.40% |
| Furniture | $741,999.80 | $18,451.27 | 2.49% |
| Office Supplies | $719,047.03 | $122,490.80 | 17.04% |

### By Region

| Region | Sales | Profit |
|---|---:|---:|
| West | $725,457.82 | $108,418.45 |
| East | $678,781.24 | $91,522.78 |
| Central | $501,239.89 | $39,706.36 |
| South | $391,721.91 | $46,749.43 |

### Yearly Sales (approx.)

| Year | Sales |
|---|---:|
| 2014 | $484,247 |
| 2015 | $470,533 |
| 2016 | $609,206 |
| 2017 | $733,215 |

### Other Observations

- **Tables** generated a loss of approximately **-$17,725**.
- **Seasonality:** November had the highest monthly sales (about $352,461), December was also strong, and September–December was generally a strong period. February had the lowest monthly sales.
- **Discounts:** higher discount levels were *associated with* lower profitability. This is an observed association in the data and does not show that discounts caused the lower profit.

## 🗄 SQL Analysis

SQLite was used to answer practical business questions rather than just practice syntax. Queries covered:

- Sales by region and by category
- Profit margin by category
- Top 10 products by sales and by profit
- Bottom 10 products by profit
- Sales and profit by segment
- Top customers
- Average order value
- Orders by year
- Monthly sales and profit
- High-discount transactions with negative profit
- Regions with negative profit
- Category performance by year

## ⏳ Time Series Analysis

Monthly sales data was created for **January 2014 to December 2017 (48 months)**. The analysis included:

- Monthly sales
- 3-month and 6-month moving averages
- Seasonality
- Yearly sales
- Month-over-month growth
- Year-over-year growth
- Highest and lowest sales months
- Overall sales growth

Output: `data/processed/monthly_sales_timeseries.csv`

## 🔮 Forecasting

Three approaches were evaluated:

1. **Baseline**
2. **Linear Regression**
3. **Seasonal Regression**

The **first 36 months were used for training** and the **final 12 months for testing**. The workflow included the train/test split, baseline forecasting, linear regression, seasonal regression, an actual vs predicted comparison, and a future 12-month forecast.

Output: `data/processed/future_sales_forecast.csv`

## 📏 Model Evaluation

Models were compared using **MAE**, **RMSE**, and **MAPE**.

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Baseline | 22,668.13 | 31,241.81 | 35.13% |
| Linear Regression | 19,663.55 | 23,664.50 | 44.41% |
| **Seasonal Regression** | **12,180.97** | **16,833.86** | **21.21%** |

✅ **Selected model: Seasonal Regression**, because it produced the lowest MAE, RMSE, and MAPE among the evaluated models.

> Note: Linear Regression had a lower MAE and RMSE than the Baseline but a higher MAPE, which is why comparing several metrics together is useful. These results come from a single 12-month test period on one dataset.

Output: `data/processed/model_evaluation_results.csv`

## 💡 Key Findings

1. Technology was the strongest category in both sales and profit.
2. Technology generated approximately **$836K** in sales and **$145K** in profit.
3. West was the strongest region by sales at approximately **$725K**.
4. Furniture had a much lower profit margin (2.49%) than Technology and Office Supplies.
5. Tables generated approximately **-$17.7K** in profit.
6. Higher discount levels were associated with lower profitability.
7. Sales showed seasonal strength toward September–December.
8. November was the highest-sales month in the full dataset.
9. Seasonal Regression had the best forecasting performance among the tested models.

## ✅ Business Recommendations

The following are recommendations based on this analysis, not guaranteed outcomes:

1. Investigate Furniture profitability.
2. Review discounting strategies, especially for high-discount transactions.
3. Investigate loss-making sub-categories such as Tables.
4. Continue supporting strong-performing regions such as West.
5. Prepare inventory and business resources ahead of peak seasonal periods.
6. Use the sales forecast to support planning and decision-making.

## 🖥 Streamlit Dashboard

An interactive Streamlit dashboard was built as an additional layer on top of the analytical work, so the results can be explored without running any code.

🚀 **Live demo:** [Open the dashboard](https://sales-forecasting-for-businesses-xwvfj9o7bje8zzgdqm75n4.streamlit.app/)

**Sections**

1. Business Overview
2. Sales Analysis
3. Product Analysis
4. Regional & Customer Analysis
5. Sales Forecast
6. Model Performance
7. Business Recommendations

**Features:** KPI cards, interactive Plotly charts, sales / profit / category / sub-category / regional / customer analysis, forecast visualization, and model comparison.

**Filters:** Year, Region, Category, Sub-Category, Segment, Ship Mode.

## 📊 Power BI Dashboard

Power BI was used to create interactive business dashboards for communicating the analysis. It is kept as a **separate BI dashboard** and was not replaced by Streamlit. The two serve as complementary presentation layers. See the screenshots below.

## 📸 Screenshots / Demo

### Streamlit Dashboard

#### Business Overview

![Business Overview](screenshots/Business-Overview-%28Streamlit%29.png)

#### Sales Analysis

![Sales Analysis](screenshots/Sales-Analysis-%28Streamlit%29.png)

#### Product Analysis

![Product Analysis](screenshots/Product-Analysis-%28Streamlit%29.png)

#### Regional & Customer Analysis

![Regional & Customer Analysis](screenshots/Regional_%26_Customer-Analysis-%28Streamlit%29.png)

#### Sales Forecast

![Sales Forecast](screenshots/Sales-Forecast-%28Streamlit%29.png)

#### Model Performance

![Model Performance](screenshots/Model-Performance-%28Streamlit%29.png)

#### Business Recommendations

![Business Recommendations](screenshots/Business-Recommendations-%28Streamlit%29.png)

### Power BI Dashboard

#### Overview

![Power BI Overview](screenshots/Overview_%28Power%20BI%29.png)

#### Sales Forecast Dashboard

![Power BI Sales Forecast](screenshots/Sales-Forecast-Dashboard-%28Power%20BI%29.png)

## 🗂 Project Structure

```
Sales-Forecasting-for-Businesses/
│
├── data/
│   ├── raw/
│   │   └── Sample - Superstore.csv
│   ├── messy/
│   │   └── sales_messy.csv
│   └── processed/
│       ├── sales_cleaned.csv
│       ├── monthly_sales_timeseries.csv
│       ├── future_sales_forecast.csv
│       ├── model_evaluation_results.csv
│       └── sales_messy_practice_cleaned.csv
│
├── screenshots/
│   ├── Business-Overview-(Streamlit).png
│   ├── Business-Recommendations-(Streamlit).png
│   ├── Model-Performance-(Streamlit).png
│   ├── Overview_(Power BI).png
│   ├── Product-Analysis-(Streamlit).png
│   ├── Regional_&_Customer-Analysis-(Streamlit).png
│   ├── Sales-Analysis-(Streamlit).png
│   ├── Sales-Forecast-(Streamlit).png
│   └── Sales-Forecast-Dashboard-(Power BI).png
│
├── main.py
├── create_database.py
├── sql_queries.py
├── time_series.py
├── forecasting.py
├── model_evaluation.py
├── business_recommendations.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

**Key files**

| File | Purpose |
|---|---|
| `main.py` | Main analysis workflow (data loading, cleaning, and exploration) |
| `create_database.py` | Creates the SQLite database from the cleaned data |
| `sql_queries.py` | Runs the business-oriented SQL queries |
| `time_series.py` | Builds the monthly time series and growth/seasonality analysis |
| `forecasting.py` | Train/test split, baseline, linear and seasonal regression, and the 12-month forecast |
| `model_evaluation.py` | Calculates MAE, RMSE, and MAPE and compares the models |
| `business_recommendations.py` | Generates business recommendations from the analysis |
| `app.py` | Streamlit dashboard |

The `data/messy/` folder and `sales_messy_practice_cleaned.csv` hold a separate messy-data practice file for cleaning exercises.

## ⚙️ How to Run Locally

**1. Clone the repository**

```bash
git clone https://github.com/shubham17-web/Sales-Forecasting-for-Businesses.git
cd Sales-Forecasting-for-Businesses
```

**2. Create and activate a virtual environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run the analysis scripts**

```bash
python main.py
python create_database.py
python sql_queries.py
python time_series.py
python forecasting.py
python model_evaluation.py
python business_recommendations.py
```

**5. Launch the Streamlit dashboard**

```bash
streamlit run app.py
```

> The Power BI dashboard is a separate file and is not run through Python. It is represented by the screenshots above.

---

⭐ If you found this project useful, feel free to star the repository.
