# ============================================================
# SALES FORECASTING FOR BUSINESSES
# MAIN ANALYSIS FILE
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# 2. LOAD ORIGINAL DATASET
# ============================================================

df = pd.read_csv(
    "data/raw/Sample - Superstore.csv",
    encoding="latin1"
)

print("Original dataset loaded successfully!")


# ============================================================
# 3. BASIC DATASET UNDERSTANDING
# ============================================================

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMN NAMES ==========")
print(df.columns)

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== DATASET INFORMATION ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())


# ============================================================
# 4. UNIQUE VALUES
# ============================================================

print("\n========== UNIQUE VALUES ==========")

print("Orders:", df["Order ID"].nunique())
print("Customers:", df["Customer ID"].nunique())
print("Products:", df["Product ID"].nunique())
print("Categories:", df["Category"].nunique())
print("Sub-Categories:", df["Sub-Category"].nunique())
print("Regions:", df["Region"].nunique())
print("Segments:", df["Segment"].nunique())

print("\nCategory Values:")
print(df["Category"].unique())

print("\nRegion Values:")
print(df["Region"].unique())

print("\nSegment Values:")
print(df["Segment"].unique())


# ============================================================
# 5. DATE CONVERSION
# ============================================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%m/%d/%Y"
)

print("\n========== SALES PERIOD ==========")

print("First Order Date:", df["Order Date"].min())
print("Last Order Date:", df["Order Date"].max())


# ============================================================
# 6. CREATE MESSY DATASET FOR CLEANING PRACTICE
# ============================================================

print("\n========== CREATING MESSY DATA ==========")

# Take 100 rows from original dataset
messy_df = df.sample(
    n=100,
    random_state=42
).copy()


# ------------------------------------------------------------
# Introduce intentional problems
# ------------------------------------------------------------

# 1. Missing Customer Name
messy_df.iloc[5, messy_df.columns.get_loc("Customer Name")] = np.nan

# 2. Missing Profit
messy_df.iloc[10, messy_df.columns.get_loc("Profit")] = np.nan

# 3. Extra spaces in Category
messy_df.iloc[15, messy_df.columns.get_loc("Category")] = " Technology "

# 4. Wrong capitalization
messy_df.iloc[20, messy_df.columns.get_loc("Region")] = "west"

# 5. Invalid quantity
messy_df.iloc[25, messy_df.columns.get_loc("Quantity")] = 0

# 6. Invalid discount
messy_df.iloc[30, messy_df.columns.get_loc("Discount")] = 1.2

# 7. Invalid shipping date
messy_df.iloc[35, messy_df.columns.get_loc("Ship Date")] = (
    messy_df.iloc[35]["Order Date"] - pd.Timedelta(days=10)
)

# 8. Negative sales
messy_df.iloc[40, messy_df.columns.get_loc("Sales")] = -500

# 9. Sales stored as text
messy_df["Sales"] = messy_df["Sales"].astype(str)

messy_df.iloc[
    45,
    messy_df.columns.get_loc("Sales")
] = " 1500.50 "

# 10. Duplicate entire row
messy_df = pd.concat(
    [messy_df, messy_df.iloc[[50]]],
    ignore_index=True
)


# Create folder
os.makedirs("data/messy", exist_ok=True)


# Save messy dataset
messy_df.to_csv(
    "data/messy/sales_messy.csv",
    index=False
)

print("Messy dataset created successfully!")
print("Rows:", len(messy_df))
print("Columns:", len(messy_df.columns))


# ============================================================
# 7. INSPECT MESSY DATA
# ============================================================

print("\n========== MESSY DATA INSPECTION ==========")

print("\nMissing Values:")
print(messy_df.isnull().sum())

print("\nDuplicate Rows:")
print(messy_df.duplicated().sum())

print("\nData Types:")
print(messy_df.dtypes)

print("\nQuantity Problems:")
print((messy_df["Quantity"] <= 0).sum())

print("\nDiscount Problems:")
print(
    (
        (messy_df["Discount"] < 0)
        | (messy_df["Discount"] > 1)
    ).sum()
)

print("\nNegative Sales:")
print((pd.to_numeric(messy_df["Sales"], errors="coerce") < 0).sum())


# ============================================================
# 8. CLEANING THE MESSY DATA
# ============================================================

print("\n========== CLEANING DATA ==========")

clean_df = messy_df.copy()


# ------------------------------------------------------------
# 8.1 Remove exact duplicate rows
# ------------------------------------------------------------

before_duplicates = len(clean_df)

clean_df = clean_df.drop_duplicates()

after_duplicates = len(clean_df)

print(
    "Duplicate rows removed:",
    before_duplicates - after_duplicates
)


# ------------------------------------------------------------
# 8.2 Clean text columns
# ------------------------------------------------------------

text_columns = [
    "Order ID",
    "Ship Mode",
    "Customer ID",
    "Customer Name",
    "Segment",
    "Country",
    "City",
    "State",
    "Region",
    "Product ID",
    "Category",
    "Sub-Category",
    "Product Name"
]

for column in text_columns:
    clean_df[column] = clean_df[column].astype("string").str.strip()


# ------------------------------------------------------------
# 8.3 Standardize categorical values
# ------------------------------------------------------------

clean_df["Category"] = clean_df["Category"].replace({
    "technology": "Technology",
    "Technology": "Technology",
    "furniture": "Furniture",
    "Furniture": "Furniture",
    "office supplies": "Office Supplies",
    "Office Supplies": "Office Supplies"
})

clean_df["Region"] = clean_df["Region"].str.title()


# ------------------------------------------------------------
# 8.4 Convert numeric columns
# ------------------------------------------------------------

numeric_columns = [
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

for column in numeric_columns:
    clean_df[column] = pd.to_numeric(
        clean_df[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 8.5 Convert dates
# ------------------------------------------------------------

clean_df["Order Date"] = pd.to_datetime(
    clean_df["Order Date"],
    errors="coerce"
)

clean_df["Ship Date"] = pd.to_datetime(
    clean_df["Ship Date"],
    errors="coerce"
)


# ------------------------------------------------------------
# 8.6 Handle missing values
# ------------------------------------------------------------

# Customer Name is descriptive information.
clean_df["Customer Name"] = clean_df["Customer Name"].fillna(
    "Unknown"
)

# Profit is an important numerical measure.
# Remove rows where profit is completely missing.
clean_df = clean_df.dropna(
    subset=["Profit"]
)


# ------------------------------------------------------------
# 8.7 Remove invalid sales
# ------------------------------------------------------------

clean_df = clean_df[
    clean_df["Sales"] > 0
]


# ------------------------------------------------------------
# 8.8 Remove invalid quantities
# ------------------------------------------------------------

clean_df = clean_df[
    clean_df["Quantity"] > 0
]


# ------------------------------------------------------------
# 8.9 Remove invalid discounts
# ------------------------------------------------------------

clean_df = clean_df[
    (clean_df["Discount"] >= 0)
    & (clean_df["Discount"] <= 1)
]


# ------------------------------------------------------------
# 8.10 Validate shipping dates
# ------------------------------------------------------------

clean_df = clean_df[
    clean_df["Ship Date"] >= clean_df["Order Date"]
]


# ============================================================
# 9. FINAL DATA VALIDATION
# ============================================================

print("\n========== FINAL VALIDATION ==========")

print("Rows:", len(clean_df))
print("Columns:", len(clean_df.columns))

print(
    "Missing Values:",
    clean_df.isnull().sum().sum()
)

print(
    "Duplicate Rows:",
    clean_df.duplicated().sum()
)

print(
    "Negative Sales:",
    (clean_df["Sales"] < 0).sum()
)

print(
    "Invalid Quantity:",
    (clean_df["Quantity"] <= 0).sum()
)

print(
    "Invalid Discount:",
    (
        (clean_df["Discount"] < 0)
        | (clean_df["Discount"] > 1)
    ).sum()
)

invalid_ship_dates = clean_df[
    clean_df["Ship Date"] < clean_df["Order Date"]
]

print(
    "Invalid Shipping Dates:",
    len(invalid_ship_dates)
)

print("\nFinal Data Types:")
print(clean_df.dtypes)


# ============================================================
# 10. SAVE CLEAN DATASET
# ============================================================

os.makedirs("data/processed", exist_ok=True)

clean_df.to_csv(
    "data/processed/sales_cleaned.csv",
    index=False
)

print("\nClean dataset saved successfully!")


# ============================================================
# 11. BUSINESS KPIs
# ============================================================

print("\n========== BUSINESS KPIs ==========")

print("Total Sales:", clean_df["Sales"].sum())
print("Total Profit:", clean_df["Profit"].sum())
print("Total Quantity Sold:", clean_df["Quantity"].sum())
print("Total Orders:", clean_df["Order ID"].nunique())
print("Total Customers:", clean_df["Customer ID"].nunique())
print("Total Products:", clean_df["Product ID"].nunique())


# ============================================================
# 12. SALES BY CATEGORY
# ============================================================

print("\n========== SALES BY CATEGORY ==========")

category_sales = (
    clean_df
    .groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(category_sales)


# ============================================================
# 13. SALES BY SUB-CATEGORY
# ============================================================

print("\n========== SALES BY SUB-CATEGORY ==========")

subcategory_sales = (
    clean_df
    .groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(subcategory_sales)


# ============================================================
# 14. PROFIT BY CATEGORY
# ============================================================

print("\n========== PROFIT BY CATEGORY ==========")

category_profit = (
    clean_df
    .groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(category_profit)


# ============================================================
# 15. PROFIT BY SUB-CATEGORY
# ============================================================

print("\n========== PROFIT BY SUB-CATEGORY ==========")

subcategory_profit = (
    clean_df
    .groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(subcategory_profit)


# ============================================================
# 16. SALES BY REGION
# ============================================================

print("\n========== SALES BY REGION ==========")

region_sales = (
    clean_df
    .groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(region_sales)


# ============================================================
# 17. PROFIT BY REGION
# ============================================================

print("\n========== PROFIT BY REGION ==========")

region_profit = (
    clean_df
    .groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(region_profit)


# ============================================================
# 18. DISCOUNT ANALYSIS
# ============================================================

print("\n========== DISCOUNT ANALYSIS ==========")

discount_profit = (
    clean_df
    .groupby("Discount")["Profit"]
    .sum()
    .sort_index()
)

print(discount_profit)


# ============================================================
# 19. TIME-BASED ANALYSIS
# ============================================================

print("\n========== TIME-BASED ANALYSIS ==========")

clean_df["Year"] = clean_df["Order Date"].dt.year
clean_df["Month"] = clean_df["Order Date"].dt.month


# ------------------------------------------------------------
# Yearly Sales
# ------------------------------------------------------------

yearly_sales = (
    clean_df
    .groupby("Year")["Sales"]
    .sum()
)

print("\n========== YEARLY SALES ==========")
print(yearly_sales)


# ------------------------------------------------------------
# Monthly Sales
# ------------------------------------------------------------

monthly_sales = (
    clean_df
    .groupby("Month")["Sales"]
    .sum()
)

print("\n========== MONTHLY SALES ==========")
print(monthly_sales)


# ------------------------------------------------------------
# Monthly Profit
# ------------------------------------------------------------

monthly_profit = (
    clean_df
    .groupby("Month")["Profit"]
    .sum()
)

print("\n========== MONTHLY PROFIT ==========")
print(monthly_profit)


# ============================================================
# 20. PROFIT MARGIN BY CATEGORY
# ============================================================

category_summary = (
    clean_df
    .groupby("Category")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

category_summary["Profit_Margin"] = (
    category_summary["Profit"]
    / category_summary["Sales"]
) * 100

print("\n========== CATEGORY PROFIT MARGIN ==========")

print(
    category_summary
    .sort_values("Profit_Margin", ascending=False)
)


# ============================================================
# 21. VISUALIZATION — YEARLY SALES
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    yearly_sales.index,
    yearly_sales.values,
    marker="o"
)

plt.title("Yearly Sales Trend")
plt.xlabel("Year")
plt.ylabel("Sales")

plt.grid(True)
plt.show()


# ============================================================
# 22. VISUALIZATION — MONTHLY SALES
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(range(1, 13))
plt.grid(True)

plt.show()


# ============================================================
# 23. VISUALIZATION — SALES BY CATEGORY
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    category_sales.index,
    category_sales.values
)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.grid(axis="y")
plt.show()


# ============================================================
# 24. VISUALIZATION — PROFIT BY CATEGORY
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    category_profit.index,
    category_profit.values
)

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")

plt.grid(axis="y")
plt.show()


# ============================================================
# 25. VISUALIZATION — PROFIT BY REGION
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    region_profit.index,
    region_profit.values
)

plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")

plt.grid(axis="y")
plt.show()


# ============================================================
# 26. VISUALIZATION — DISCOUNT VS PROFIT
# ============================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    clean_df["Discount"],
    clean_df["Profit"],
    alpha=0.5
)

plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")

plt.grid(True)
plt.show()


# ============================================================
# 27. VISUALIZATION — MONTHLY PROFIT
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_profit.index,
    monthly_profit.values,
    marker="o"
)

plt.title("Monthly Profit Trend")
plt.xlabel("Month")
plt.ylabel("Profit")

plt.xticks(range(1, 13))
plt.grid(True)

plt.show()


# ============================================================
# 28. VISUALIZATION — SALES BY SUB-CATEGORY
# ============================================================

plt.figure(figsize=(10, 7))

plt.barh(
    subcategory_sales.index,
    subcategory_sales.values
)

plt.title("Sales by Sub-Category")
plt.xlabel("Sales")
plt.ylabel("Sub-Category")

plt.grid(axis="x")
plt.show()


# ============================================================
# 29. VISUALIZATION — PROFIT BY SUB-CATEGORY
# ============================================================

plt.figure(figsize=(10, 7))

plt.barh(
    subcategory_profit.index,
    subcategory_profit.values
)

plt.title("Profit by Sub-Category")
plt.xlabel("Profit")
plt.ylabel("Sub-Category")

plt.grid(axis="x")
plt.show()


# ============================================================
# END OF STAGE 3
# ============================================================

print("\n================================================")
print("STAGE 3 — EDA COMPLETED")
print("================================================")