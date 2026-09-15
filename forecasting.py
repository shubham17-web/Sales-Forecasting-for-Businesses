import pandas as pd


# ============================================================
# STEP 6.1 — LOAD TIME SERIES DATA
# ============================================================

df = pd.read_csv(
    "data/processed/monthly_sales_timeseries.csv"
)

# Convert date column
df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)

# Sort by date
df = df.sort_values(
    "Order Date"
).reset_index(drop=True)


print("\n========== FORECASTING DATA ==========")

print(df.head())

print("\nLast 5 Months:")
print(df.tail())

print("\nRows:", len(df))


# ============================================================
# SELECT REQUIRED COLUMNS
# ============================================================

forecast_df = df[
    [
        "Order Date",
        "Sales"
    ]
].copy()


print("\n========== FORECAST DATASET ==========")

print(forecast_df.head())

print("\nRows:", len(forecast_df))
print("Columns:", len(forecast_df.columns))


# ============================================================
# FINAL CHECK
# ============================================================

print("\n========== DATA VALIDATION ==========")

print(
    "Missing Dates:",
    forecast_df["Order Date"].isnull().sum()
)

print(
    "Missing Sales:",
    forecast_df["Sales"].isnull().sum()
)

print(
    "Duplicate Dates:",
    forecast_df["Order Date"].duplicated().sum()
)

print(
    "Negative Sales:",
    (forecast_df["Sales"] < 0).sum()
)


print("\nForecasting dataset prepared successfully!")

# ============================================================
# STEP 6.2 — TRAIN / TEST SPLIT
# ============================================================

# First 36 months → Training data
train = forecast_df.iloc[:36].copy()

# Last 12 months → Testing data
test = forecast_df.iloc[-12:].copy()


print("\n========== TRAIN / TEST SPLIT ==========")

print("Training Data:")
print("Start:", train["Order Date"].min())
print("End:", train["Order Date"].max())
print("Rows:", len(train))

print("\nTesting Data:")
print("Start:", test["Order Date"].min())
print("End:", test["Order Date"].max())
print("Rows:", len(test))


# ============================================================
# CHECK SPLIT
# ============================================================

print("\n========== SPLIT VALIDATION ==========")

print("Total Rows:", len(forecast_df))
print("Train Rows:", len(train))
print("Test Rows:", len(test))

print(
    "Rows Match:",
    len(train) + len(test) == len(forecast_df)
)

# ============================================================
# STEP 6.3 — BASELINE FORECAST
# ============================================================

# Calculate average monthly sales from training data
baseline_value = train["Sales"].mean()

print("\n========== BASELINE FORECAST ==========")

print(
    "Average Training Sales:",
    round(baseline_value, 2)
)


# Use the average as the prediction for every test month
test["Baseline_Forecast"] = baseline_value


print("\nBaseline Predictions:")

print(
    test[
        [
            "Order Date",
            "Sales",
            "Baseline_Forecast"
        ]
    ]
)


# ============================================================
# BASELINE ERROR
# ============================================================

# Calculate Mean Absolute Error (MAE)

mae_baseline = (
    abs(
        test["Sales"]
        - test["Baseline_Forecast"]
    ).mean()
)


print("\n========== BASELINE PERFORMANCE ==========")

print(
    "Baseline MAE:",
    round(mae_baseline, 2)
)

# ============================================================
# STEP 6.4 — LINEAR REGRESSION FORECASTING
# ============================================================

from sklearn.linear_model import LinearRegression


# Create month numbers
# 0 = first month, 1 = second month, etc.
train["Month_Number"] = range(len(train))

test["Month_Number"] = range(
    len(train),
    len(train) + len(test)
)


# ============================================================
# CREATE MODEL
# ============================================================

model = LinearRegression()


# Training data
X_train = train[
    ["Month_Number"]
]

y_train = train[
    "Sales"
]


# Train the model
model.fit(
    X_train,
    y_train
)


print("\n========== LINEAR REGRESSION MODEL ==========")

print(
    "Model trained successfully!"
)

print(
    "Slope:",
    round(model.coef_[0], 2)
)

print(
    "Intercept:",
    round(model.intercept_, 2)
)


# ============================================================
# MAKE PREDICTIONS
# ============================================================

test["Linear_Forecast"] = model.predict(
    test[
        ["Month_Number"]
    ]
)


print("\n========== LINEAR REGRESSION FORECAST ==========")

print(
    test[
        [
            "Order Date",
            "Sales",
            "Linear_Forecast"
        ]
    ]
)


# ============================================================
# CALCULATE MODEL ERROR
# ============================================================

mae_linear = (
    abs(
        test["Sales"]
        - test["Linear_Forecast"]
    ).mean()
)


print("\n========== LINEAR REGRESSION PERFORMANCE ==========")

print(
    "Linear Regression MAE:",
    round(mae_linear, 2)
)

print(
    "Baseline MAE:",
    round(mae_baseline, 2)
)


# ============================================================
# COMPARE BASELINE VS MODEL
# ============================================================

if mae_linear < mae_baseline:

    print(
        "\nLinear Regression performed better than the baseline."
    )

else:

    print(
        "\nBaseline performed better than Linear Regression."
    )

    # ============================================================
# STEP 6.5 — ACTUAL VS FORECAST VISUALIZATION
# ============================================================

import matplotlib.pyplot as plt


plt.figure(figsize=(12, 6))

# Actual sales
plt.plot(
    test["Order Date"],
    test["Sales"],
    marker="o",
    label="Actual Sales"
)

# Baseline forecast
plt.plot(
    test["Order Date"],
    test["Baseline_Forecast"],
    linestyle="--",
    label="Baseline Forecast"
)

# Linear regression forecast
plt.plot(
    test["Order Date"],
    test["Linear_Forecast"],
    marker="o",
    linestyle="--",
    label="Linear Regression Forecast"
)


plt.title("Actual vs Forecasted Sales — 2017")

plt.xlabel("Date")
plt.ylabel("Sales")

plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# ============================================================
# STEP 6.6 — SEASONAL FORECASTING
# ============================================================

# Create month-of-year feature
train["Month"] = train["Order Date"].dt.month
test["Month"] = test["Order Date"].dt.month


# ============================================================
# CREATE SEASONAL MODEL
# ============================================================

seasonal_model = LinearRegression()


# Use both trend and month
X_train_seasonal = train[
    ["Month_Number", "Month"]
]

y_train_seasonal = train[
    "Sales"
]


# Train model
seasonal_model.fit(
    X_train_seasonal,
    y_train_seasonal
)


print("\n========== SEASONAL LINEAR REGRESSION ==========")

print("Seasonal model trained successfully!")


# ============================================================
# MAKE SEASONAL FORECAST
# ============================================================

test["Seasonal_Forecast"] = (
    seasonal_model.predict(
        test[
            ["Month_Number", "Month"]
        ]
    )
)


print("\n========== SEASONAL FORECAST ==========")

print(
    test[
        [
            "Order Date",
            "Sales",
            "Linear_Forecast",
            "Seasonal_Forecast"
        ]
    ]
)


# ============================================================
# CALCULATE ERROR
# ============================================================

mae_seasonal = (
    abs(
        test["Sales"]
        - test["Seasonal_Forecast"]
    ).mean()
)


print("\n========== MODEL COMPARISON ==========")

print(
    "Baseline MAE:",
    round(mae_baseline, 2)
)

print(
    "Linear Regression MAE:",
    round(mae_linear, 2)
)

print(
    "Seasonal Regression MAE:",
    round(mae_seasonal, 2)
)

# ============================================================
# STEP 6.7 — FUTURE 12-MONTH FORECAST
# ============================================================

# Create future dates
future_dates = pd.date_range(
    start=test["Order Date"].max() + pd.offsets.MonthBegin(1),
    periods=12,
    freq="MS"
)

# Create future month numbers
future_month_numbers = range(
    len(forecast_df),
    len(forecast_df) + 12
)

# Create future dataframe
future_df = pd.DataFrame({
    "Order Date": future_dates,
    "Month_Number": list(future_month_numbers)
})

# Extract month number
future_df["Month"] = (
    future_df["Order Date"].dt.month
)


# ============================================================
# PREDICT FUTURE SALES
# ============================================================

future_df["Forecasted_Sales"] = (
    seasonal_model.predict(
        future_df[
            [
                "Month_Number",
                "Month"
            ]
        ]
    )
)


print("\n========== NEXT 12 MONTH FORECAST ==========")

print(
    future_df[
        [
            "Order Date",
            "Forecasted_Sales"
        ]
    ]
)


# ============================================================
# SAVE FUTURE FORECAST
# ============================================================

future_df.to_csv(
    "data/processed/future_sales_forecast.csv",
    index=False
)

print(
    "\nFuture forecast saved successfully!"
)

print(
    "File:",
    "data/processed/future_sales_forecast.csv"
)

# ============================================================
# STEP 6.8 — FINAL FORECAST VISUALIZATION
# ============================================================

plt.figure(figsize=(14, 7))

# Historical sales
plt.plot(
    forecast_df["Order Date"],
    forecast_df["Sales"],
    label="Historical Sales"
)

# Future forecast
plt.plot(
    future_df["Order Date"],
    future_df["Forecasted_Sales"],
    marker="o",
    linestyle="--",
    label="Future Forecast"
)

plt.title("Historical Sales and Future Sales Forecast")

plt.xlabel("Date")
plt.ylabel("Sales")

plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# FINAL FORECAST SUMMARY
# ============================================================

print("\n========== FINAL FORECAST SUMMARY ==========")

print(
    "Forecast Start:",
    future_df["Order Date"].min().strftime("%B %Y")
)

print(
    "Forecast End:",
    future_df["Order Date"].max().strftime("%B %Y")
)

print(
    "Average Forecasted Monthly Sales:",
    round(
        future_df["Forecasted_Sales"].mean(),
        2
    )
)

print(
    "Total Forecasted Sales:",
    round(
        future_df["Forecasted_Sales"].sum(),
        2
    )
)

print("\n==============================================")
print("       STAGE 6 FORECASTING COMPLETE")
print("==============================================")