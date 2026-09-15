import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# STEP 1 — LOAD CLEAN DATA
# ============================================================

df = pd.read_csv(
    "data/processed/sales_cleaned.csv"
)

# Convert Order Date
df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)

print("\n========== DATA LOADED ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# STEP 2 — CREATE MONTHLY SALES DATA
# ============================================================

monthly_sales = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

# Convert Period to timestamp
monthly_sales["Order Date"] = (
    monthly_sales["Order Date"].dt.to_timestamp()
)

# Sort by date
monthly_sales = monthly_sales.sort_values(
    "Order Date"
)

print("\n========== MONTHLY SALES ==========")
print(monthly_sales)

print("\nTotal Months:", len(monthly_sales))


# ============================================================
# STEP 3 — TIME SERIES VALIDATION
# ============================================================

expected_months = pd.date_range(
    start=monthly_sales["Order Date"].min(),
    end=monthly_sales["Order Date"].max(),
    freq="MS"
)

missing_months = expected_months.difference(
    monthly_sales["Order Date"]
)

print("\n========== TIME SERIES VALIDATION ==========")

print(
    "First Month:",
    monthly_sales["Order Date"].min()
)

print(
    "Last Month:",
    monthly_sales["Order Date"].max()
)

print(
    "Total Months:",
    len(monthly_sales)
)

print(
    "Missing Months:",
    len(missing_months)
)

if len(missing_months) == 0:
    print("Time series has no missing months.")
else:
    print("Missing Months:")
    print(missing_months)


# ============================================================
# STEP 4 — VISUALIZE MONTHLY SALES
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["Order Date"],
    monthly_sales["Sales"]
)

plt.title("Monthly Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 5 — MOVING AVERAGES
# ============================================================

monthly_sales["3_Month_MA"] = (
    monthly_sales["Sales"]
    .rolling(window=3)
    .mean()
)

monthly_sales["6_Month_MA"] = (
    monthly_sales["Sales"]
    .rolling(window=6)
    .mean()
)

print("\n========== MOVING AVERAGES ==========")

print(
    monthly_sales[
        [
            "Order Date",
            "Sales",
            "3_Month_MA",
            "6_Month_MA"
        ]
    ].tail(12)
)


# ============================================================
# STEP 6 — VISUALIZE MOVING AVERAGES
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["Order Date"],
    monthly_sales["Sales"],
    label="Monthly Sales"
)

plt.plot(
    monthly_sales["Order Date"],
    monthly_sales["3_Month_MA"],
    label="3-Month Moving Average"
)

plt.plot(
    monthly_sales["Order Date"],
    monthly_sales["6_Month_MA"],
    label="6-Month Moving Average"
)

plt.title("Monthly Sales with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 7 — MONTHLY SEASONALITY
# ============================================================

monthly_sales["Month"] = (
    monthly_sales["Order Date"].dt.month
)

monthly_sales["Month_Name"] = (
    monthly_sales["Order Date"]
    .dt.strftime("%b")
)

seasonality = (
    monthly_sales
    .groupby(
        ["Month", "Month_Name"]
    )["Sales"]
    .mean()
    .reset_index()
    .sort_values("Month")
)

print("\n========== MONTHLY SEASONALITY ==========")

print(seasonality)


# ============================================================
# STEP 8 — VISUALIZE SEASONALITY
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    seasonality["Month_Name"],
    seasonality["Sales"],
    marker="o"
)

plt.title("Average Sales by Month")
plt.xlabel("Month")
plt.ylabel("Average Sales")

plt.tight_layout()
plt.show()


# ============================================================
# STEP 9 — YEARLY SALES
# ============================================================

df["Year"] = (
    df["Order Date"].dt.year
)

yearly_sales = (
    df.groupby("Year")["Sales"]
    .sum()
    .reset_index()
)

print("\n========== YEARLY SALES ==========")

print(yearly_sales)


# ============================================================
# STEP 10 — YEAR-OVER-YEAR GROWTH
# ============================================================

yearly_sales["YoY_Growth_%"] = (
    yearly_sales["Sales"]
    .pct_change()
    * 100
)

print("\n========== YEAR-OVER-YEAR GROWTH ==========")

print(yearly_sales)


# ============================================================
# STEP 11 — VISUALIZE YEARLY GROWTH
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    yearly_sales["Year"],
    yearly_sales["Sales"],
    marker="o"
)

plt.title("Yearly Sales Growth")
plt.xlabel("Year")
plt.ylabel("Sales")

plt.xticks(
    yearly_sales["Year"]
)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 12 — MONTH-OVER-MONTH GROWTH
# ============================================================

monthly_sales["MoM_Growth_%"] = (
    monthly_sales["Sales"]
    .pct_change()
    * 100
)

print("\n========== MONTH-OVER-MONTH GROWTH ==========")

print(
    monthly_sales[
        [
            "Order Date",
            "Sales",
            "MoM_Growth_%"
        ]
    ].tail(12)
)


# ============================================================
# STEP 13 — FIND HIGHEST AND LOWEST SALES MONTHS
# ============================================================

highest_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmax()
]

lowest_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmin()
]

print("\n========== SALES EXTREMES ==========")

print(
    "Highest Sales Month:",
    highest_month["Order Date"].strftime("%B %Y")
)

print(
    "Highest Sales:",
    round(highest_month["Sales"], 2)
)

print(
    "Lowest Sales Month:",
    lowest_month["Order Date"].strftime("%B %Y")
)

print(
    "Lowest Sales:",
    round(lowest_month["Sales"], 2)
)


# ============================================================
# STEP 14 — TREND ANALYSIS
# ============================================================

first_year_sales = yearly_sales.iloc[0]["Sales"]
last_year_sales = yearly_sales.iloc[-1]["Sales"]

overall_growth = (
    (last_year_sales - first_year_sales)
    / first_year_sales
) * 100

print("\n========== OVERALL TREND ==========")

print(
    "First Year Sales:",
    round(first_year_sales, 2)
)

print(
    "Last Year Sales:",
    round(last_year_sales, 2)
)

print(
    "Overall Growth:",
    round(overall_growth, 2),
    "%"
)


# ============================================================
# STEP 15 — SAVE TIME SERIES DATA
# ============================================================

monthly_sales.to_csv(
    "data/processed/monthly_sales_timeseries.csv",
    index=False
)

print(
    "\nTime series dataset saved successfully!"
)

print(
    "File:",
    "data/processed/monthly_sales_timeseries.csv"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n==============================================")
print("       TIME SERIES ANALYSIS COMPLETE")
print("==============================================")

print("Months Analyzed:", len(monthly_sales))
print(
    "Missing Months:",
    len(missing_months)
)

print(
    "Overall Sales Growth:",
    round(overall_growth, 2),
    "%"
)

print(
    "Highest Sales Month:",
    highest_month["Order Date"].strftime("%B %Y")
)

print(
    "Lowest Sales Month:",
    lowest_month["Order Date"].strftime("%B %Y")
)

print("==============================================")