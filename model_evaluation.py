import pandas as pd


# ============================================================
# STEP 7.1 — LOAD FORECASTING DATA
# ============================================================

df = pd.read_csv(
    "data/processed/monthly_sales_timeseries.csv"
)

df["Order Date"] = pd.to_datetime(
    df["Order Date"]
)

df = df.sort_values(
    "Order Date"
).reset_index(drop=True)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

train = df.iloc[:36].copy()
test = df.iloc[36:].copy()


print("\n========== TRAIN / TEST DATA ==========")

print("Training Rows:", len(train))
print("Testing Rows:", len(test))


# ============================================================
# CREATE MONTH FEATURES
# ============================================================

train["Month_Number"] = range(
    len(train)
)

test["Month_Number"] = range(
    len(train),
    len(train) + len(test)
)

train["Month"] = train["Order Date"].dt.month
test["Month"] = test["Order Date"].dt.month


# ============================================================
# LOAD MODELS
# ============================================================

from sklearn.linear_model import LinearRegression


# -------------------------
# BASELINE
# -------------------------

baseline_value = train["Sales"].mean()

test["Baseline_Forecast"] = baseline_value


# -------------------------
# LINEAR REGRESSION
# -------------------------

linear_model = LinearRegression()

linear_model.fit(
    train[["Month_Number"]],
    train["Sales"]
)

test["Linear_Forecast"] = (
    linear_model.predict(
        test[["Month_Number"]]
    )
)


# -------------------------
# SEASONAL REGRESSION
# -------------------------

seasonal_model = LinearRegression()

seasonal_model.fit(
    train[
        [
            "Month_Number",
            "Month"
        ]
    ],
    train["Sales"]
)

test["Seasonal_Forecast"] = (
    seasonal_model.predict(
        test[
            [
                "Month_Number",
                "Month"
            ]
        ]
    )
)


# ============================================================
# MAE FUNCTION
# ============================================================

def calculate_mae(actual, predicted):

    return abs(
        actual - predicted
    ).mean()


# ============================================================
# CALCULATE MAE
# ============================================================

baseline_mae = calculate_mae(
    test["Sales"],
    test["Baseline_Forecast"]
)

linear_mae = calculate_mae(
    test["Sales"],
    test["Linear_Forecast"]
)

seasonal_mae = calculate_mae(
    test["Sales"],
    test["Seasonal_Forecast"]
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n========== MAE RESULTS ==========")

print(
    "Baseline MAE:",
    round(baseline_mae, 2)
)

print(
    "Linear Regression MAE:",
    round(linear_mae, 2)
)

print(
    "Seasonal Regression MAE:",
    round(seasonal_mae, 2)
)

# ============================================================
# STEP 7.2 — RMSE
# ============================================================

import numpy as np


def calculate_rmse(actual, predicted):

    return np.sqrt(
        np.mean(
            (actual - predicted) ** 2
        )
    )


# Calculate RMSE
baseline_rmse = calculate_rmse(
    test["Sales"],
    test["Baseline_Forecast"]
)

linear_rmse = calculate_rmse(
    test["Sales"],
    test["Linear_Forecast"]
)

seasonal_rmse = calculate_rmse(
    test["Sales"],
    test["Seasonal_Forecast"]
)


# ============================================================
# DISPLAY RMSE RESULTS
# ============================================================

print("\n========== RMSE RESULTS ==========")

print(
    "Baseline RMSE:",
    round(baseline_rmse, 2)
)

print(
    "Linear Regression RMSE:",
    round(linear_rmse, 2)
)

print(
    "Seasonal Regression RMSE:",
    round(seasonal_rmse, 2)
)

# ============================================================
# STEP 7.3 — MAPE
# ============================================================

def calculate_mape(actual, predicted):

    percentage_error = (
        abs(
            (actual - predicted) / actual
        ) * 100
    )

    return percentage_error.mean()


# Calculate MAPE
baseline_mape = calculate_mape(
    test["Sales"],
    test["Baseline_Forecast"]
)

linear_mape = calculate_mape(
    test["Sales"],
    test["Linear_Forecast"]
)

seasonal_mape = calculate_mape(
    test["Sales"],
    test["Seasonal_Forecast"]
)


# ============================================================
# DISPLAY MAPE RESULTS
# ============================================================

print("\n========== MAPE RESULTS ==========")

print(
    "Baseline MAPE:",
    round(baseline_mape, 2),
    "%"
)

print(
    "Linear Regression MAPE:",
    round(linear_mape, 2),
    "%"
)

print(
    "Seasonal Regression MAPE:",
    round(seasonal_mape, 2),
    "%"
)

# ============================================================
# STEP 7.4 — MODEL COMPARISON
# ============================================================

evaluation_results = pd.DataFrame({
    "Model": [
        "Baseline",
        "Linear Regression",
        "Seasonal Regression"
    ],
    
    "MAE": [
        baseline_mae,
        linear_mae,
        seasonal_mae
    ],
    
    "RMSE": [
        baseline_rmse,
        linear_rmse,
        seasonal_rmse
    ],
    
    "MAPE_%": [
        baseline_mape,
        linear_mape,
        seasonal_mape
    ]
})


# Round the values for cleaner output
evaluation_results["MAE"] = evaluation_results["MAE"].round(2)
evaluation_results["RMSE"] = evaluation_results["RMSE"].round(2)
evaluation_results["MAPE_%"] = evaluation_results["MAPE_%"].round(2)


print("\n========== MODEL COMPARISON ==========")
print(evaluation_results.to_string(index=False))

# ============================================================
# STEP 7.5 — DETERMINE BEST MODEL
# ============================================================

best_model = evaluation_results.loc[
    evaluation_results["MAE"].idxmin()
]

print("\n========== BEST MODEL ==========")

print("Best Model:", best_model["Model"])
print("MAE:", best_model["MAE"])
print("RMSE:", best_model["RMSE"])
print("MAPE:", best_model["MAPE_%"], "%")

# ============================================================
# STEP 7.6 — ACTUAL VS BEST FORECAST
# ============================================================

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(
    test["Order Date"],
    test["Sales"],
    marker="o",
    label="Actual Sales"
)

plt.plot(
    test["Order Date"],
    test["Seasonal_Forecast"],
    marker="o",
    linestyle="--",
    label="Seasonal Regression Forecast"
)

plt.title("Actual vs Seasonal Regression Forecast — 2017")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# ============================================================
# STEP 7.7 — SAVE EVALUATION RESULTS
# ============================================================

evaluation_results.to_csv(
    "data/processed/model_evaluation_results.csv",
    index=False
)

print("\nModel evaluation results saved successfully!")