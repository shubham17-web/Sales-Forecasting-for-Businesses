import pandas as pd
import sqlite3

# Load original raw dataset
df = pd.read_csv(
    "data/raw/Sample - Superstore.csv",
    encoding="latin1"
)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Save the main cleaned dataset
df.to_csv(
    "data/processed/sales_cleaned.csv",
    index=False
)

# Create SQLite database
connection = sqlite3.connect("sales.db")

df.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)

print("Main dataset and database restored!")
print("Rows:", len(df))

connection.close()