import sqlite3

# ============================================
# CONNECT TO DATABASE
# ============================================

connection = sqlite3.connect("sales.db")
cursor = connection.cursor()


# ============================================
# STEP 2 — SELECT
# ============================================

print("\n========== STEP 2: SELECT ==========")

cursor.execute("""
    SELECT *
    FROM sales
    LIMIT 5
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 3 — SELECT SPECIFIC COLUMNS
# ============================================

print("\n========== STEP 3: SPECIFIC COLUMNS ==========")

cursor.execute("""
    SELECT "Order ID", "Sales", "Profit"
    FROM sales
    LIMIT 10
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 4 — WHERE
# ============================================

print("\n========== STEP 4: WHERE ==========")

cursor.execute("""
    SELECT "Order ID", "Product Name", Sales, Profit
    FROM sales
    WHERE Sales > 1000
    LIMIT 10
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 5 — ORDER BY
# ============================================

print("\n========== STEP 5: ORDER BY ==========")

cursor.execute("""
    SELECT "Order ID", "Product Name", Sales, Profit
    FROM sales
    ORDER BY Sales DESC
    LIMIT 10
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 6 — GROUP BY
# ============================================

print("\n========== STEP 6: GROUP BY ==========")

cursor.execute("""
    SELECT
        Category,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Category
    ORDER BY Total_Sales DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 7 — HAVING
# ============================================

print("\n========== STEP 7: HAVING ==========")

cursor.execute("""
    SELECT
        Category,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Category
    HAVING SUM(Sales) > 700000
    ORDER BY Total_Sales DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 8 — COUNT()
# ============================================

print("\n========== STEP 8: COUNT() ==========")

cursor.execute("""
    SELECT COUNT(*) AS Total_Records
    FROM sales
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 8 — COUNT(DISTINCT)
# ============================================

print("\n========== COUNT(DISTINCT) ==========")

cursor.execute("""
    SELECT COUNT(DISTINCT "Order ID") AS Total_Orders
    FROM sales
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 8 — AVG()
# ============================================

print("\n========== AVG() ==========")

cursor.execute("""
    SELECT AVG(Sales) AS Average_Sales
    FROM sales
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 8 — MIN() AND MAX()
# ============================================

print("\n========== MIN() AND MAX() ==========")

cursor.execute("""
    SELECT
        MIN(Sales) AS Minimum_Sales,
        MAX(Sales) AS Maximum_Sales
    FROM sales
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# STEP 8 — COMBINED BUSINESS KPIs
# ============================================

print("\n========== BUSINESS KPIs ==========")

cursor.execute("""
    SELECT
        COUNT(*) AS Total_Records,
        COUNT(DISTINCT "Order ID") AS Total_Orders,
        COUNT(DISTINCT "Customer ID") AS Total_Customers,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit,
        AVG(Sales) AS Average_Sales,
        MIN(Sales) AS Minimum_Sales,
        MAX(Sales) AS Maximum_Sales
    FROM sales
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# BUSINESS QUESTION 1
# PROFIT BY CATEGORY
# ============================================

print("\n========== PROFIT BY CATEGORY ==========")

cursor.execute("""
    SELECT
        Category,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Category
    ORDER BY Total_Profit DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# BUSINESS QUESTION 2
# LOSS-MAKING SUB-CATEGORIES
# ============================================

print("\n========== LOSS-MAKING SUB-CATEGORIES ==========")

cursor.execute("""
    SELECT
        "Sub-Category",
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY "Sub-Category"
    HAVING SUM(Profit) < 0
    ORDER BY Total_Profit ASC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# BUSINESS QUESTION 3
# PROFIT BY REGION
# ============================================

print("\n========== PROFIT BY REGION ==========")

cursor.execute("""
    SELECT
        Region,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Region
    ORDER BY Total_Profit DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# BUSINESS QUESTION 4
# SALES AND PROFIT BY YEAR
# ============================================

print("\n========== SALES AND PROFIT BY YEAR ==========")

cursor.execute("""
    SELECT
        strftime('%Y', "Order Date") AS Year,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Year
    ORDER BY Year
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# BUSINESS QUESTION 5
# MONTHLY SALES
# ============================================

print("\n========== MONTHLY SALES ==========")

cursor.execute("""
    SELECT
        strftime('%m', "Order Date") AS Month,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Month
    ORDER BY Total_Sales DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================
# BUSINESS QUESTION 6
# SALES BY REGION AND CATEGORY
# ============================================

print("\n========== SALES BY REGION AND CATEGORY ==========")

cursor.execute("""
    SELECT
        Region,
        Category,
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY Region, Category
    ORDER BY Region, Total_Sales DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ============================================================
# QUESTION 7 — PROFIT MARGIN BY CATEGORY
# ============================================================

print("\n========== PROFIT MARGIN BY CATEGORY ==========")

cursor.execute("""
    SELECT
        Category,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit,
        ROUND(
            SUM(Profit) * 100.0 / SUM(Sales),
            2
        ) AS Profit_Margin
    FROM sales
    GROUP BY Category
    ORDER BY Profit_Margin DESC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 8 — TOP 10 PRODUCTS BY SALES
# ============================================================

print("\n========== TOP 10 PRODUCTS BY SALES ==========")

cursor.execute("""
    SELECT
        "Product Name",
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY "Product Name"
    ORDER BY Total_Sales DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 9 — TOP 10 PRODUCTS BY PROFIT
# ============================================================

print("\n========== TOP 10 PRODUCTS BY PROFIT ==========")

cursor.execute("""
    SELECT
        "Product Name",
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY "Product Name"
    ORDER BY Total_Profit DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 10 — BOTTOM 10 PRODUCTS BY PROFIT
# ============================================================

print("\n========== BOTTOM 10 PRODUCTS BY PROFIT ==========")

cursor.execute("""
    SELECT
        "Product Name",
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY "Product Name"
    ORDER BY Total_Profit ASC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 11 — SALES BY SEGMENT
# ============================================================

print("\n========== SALES BY SEGMENT ==========")

cursor.execute("""
    SELECT
        Segment,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Segment
    ORDER BY Total_Sales DESC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 12 — CUSTOMER ANALYSIS
# ============================================================

print("\n========== TOP 10 CUSTOMERS BY SALES ==========")

cursor.execute("""
    SELECT
        "Customer ID",
        "Customer Name",
        SUM(Sales) AS Total_Sales
    FROM sales
    GROUP BY "Customer ID", "Customer Name"
    ORDER BY Total_Sales DESC
    LIMIT 10
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 13 — AVERAGE ORDER VALUE
# ============================================================

print("\n========== AVERAGE ORDER VALUE ==========")

cursor.execute("""
    SELECT
        ROUND(
            SUM(Sales) / COUNT(DISTINCT "Order ID"),
            2
        ) AS Average_Order_Value
    FROM sales
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 14 — ORDERS BY YEAR
# ============================================================

print("\n========== ORDERS BY YEAR ==========")

cursor.execute("""
    SELECT
        strftime('%Y', "Order Date") AS Year,
        COUNT(DISTINCT "Order ID") AS Total_Orders,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Year
    ORDER BY Year
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 15 — MONTHLY SALES AND PROFIT
# ============================================================

print("\n========== MONTHLY SALES AND PROFIT ==========")

cursor.execute("""
    SELECT
        strftime('%Y-%m', "Order Date") AS Month,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Month
    ORDER BY Month
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 16 — HIGH DISCOUNT AND NEGATIVE PROFIT
# ============================================================

print("\n========== HIGH DISCOUNT + NEGATIVE PROFIT ==========")

cursor.execute("""
    SELECT
        "Sub-Category",
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    WHERE Discount >= 0.5
    GROUP BY "Sub-Category"
    HAVING SUM(Profit) < 0
    ORDER BY Total_Profit ASC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 17 — LOSS-MAKING REGIONS
# ============================================================

print("\n========== REGIONS WITH NEGATIVE PROFIT ==========")

cursor.execute("""
    SELECT
        Region,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Region
    HAVING SUM(Profit) < 0
    ORDER BY Total_Profit ASC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# QUESTION 18 — CATEGORY + YEAR
# ============================================================

print("\n========== CATEGORY PERFORMANCE BY YEAR ==========")

cursor.execute("""
    SELECT
        strftime('%Y', "Order Date") AS Year,
        Category,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM sales
    GROUP BY Year, Category
    ORDER BY Year, Total_Sales DESC
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

print("\n========== SQL ANALYSIS COMPLETE ==========")