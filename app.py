import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Sales Forecasting & Business Analytics",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# DASHBOARD STYLE
# ==================================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.25);
    }

    /* Metric values */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
    }

    /* Section spacing */
    h1 {
        margin-bottom: 10px;
    }

    h2 {
        margin-top: 25px;
    }

    h3 {
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SETTINGS
# ==================================================

# Add your Power BI link here later.
# Example:
# POWER_BI_URL = "https://app.powerbi.com/..."
POWER_BI_URL = ""


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():

    file_path = "data/processed/sales_cleaned.csv"

    df = pd.read_csv(file_path)

    # Convert date columns
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df


@st.cache_data
def load_forecast():

    file_path = "data/processed/future_sales_forecast.csv"

    return pd.read_csv(file_path)


@st.cache_data
def load_model_results():

    file_path = "data/processed/model_evaluation_results.csv"

    return pd.read_csv(file_path)


# ==================================================
# LOAD MAIN DATA
# ==================================================

try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "sales_cleaned.csv was not found. "
        "Please check data/processed/sales_cleaned.csv."
    )

    st.stop()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("📊 Sales Analytics")

st.sidebar.caption(
    "Interactive Business Dashboard"
)


# ==================================================
# NAVIGATION
# ==================================================

st.sidebar.header("📌 Dashboard")

page = st.sidebar.radio(
    "Go to",
    [
        "Business Overview",
        "Sales Analysis",
        "Product Analysis",
        "Regional & Customer Analysis",
        "Sales Forecast",
        "Model Performance",
        "Business Recommendations"
    ]
)


# ==================================================
# FILTERS
# ==================================================

st.sidebar.divider()

st.sidebar.subheader("🔎 Filters")


# Year
years = sorted(
    df["Order Date"].dt.year.unique()
)

selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + years
)


# Region
regions = sorted(
    df["Region"].dropna().unique()
)

selected_region = st.sidebar.selectbox(
    "Region",
    ["All"] + regions
)


# Category
categories = sorted(
    df["Category"].dropna().unique()
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories
)


# Sub-category
sub_categories = sorted(
    df["Sub-Category"].dropna().unique()
)

selected_sub_category = st.sidebar.selectbox(
    "Sub-Category",
    ["All"] + sub_categories
)


# Segment
segments = sorted(
    df["Segment"].dropna().unique()
)

selected_segment = st.sidebar.selectbox(
    "Segment",
    ["All"] + segments
)


# Ship Mode
ship_modes = sorted(
    df["Ship Mode"].dropna().unique()
)

selected_ship_mode = st.sidebar.selectbox(
    "Ship Mode",
    ["All"] + ship_modes
)


# ==================================================
# APPLY FILTERS
# ==================================================

filtered_df = df.copy()


if selected_year != "All":

    filtered_df = filtered_df[
        filtered_df["Order Date"].dt.year == selected_year
    ]


if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


if selected_sub_category != "All":

    filtered_df = filtered_df[
        filtered_df["Sub-Category"] == selected_sub_category
    ]


if selected_segment != "All":

    filtered_df = filtered_df[
        filtered_df["Segment"] == selected_segment
    ]


if selected_ship_mode != "All":

    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == selected_ship_mode
    ]


# ==================================================
# FILTER SUMMARY
# ==================================================

st.sidebar.divider()

st.sidebar.caption(
    f"Records after filters: {len(filtered_df):,}"
)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def money(value):

    return f"${value:,.0f}"


def number(value):

    return f"{value:,.0f}"


def calculate_kpis(data):

    total_sales = data["Sales"].sum()

    total_profit = data["Profit"].sum()

    if total_sales != 0:

        profit_margin = (
            total_profit / total_sales
        ) * 100

    else:

        profit_margin = 0


    total_orders = data["Order ID"].nunique()

    total_customers = data["Customer ID"].nunique()

    total_products = data["Product Name"].nunique()

    total_quantity = data["Quantity"].sum()


    return (
        total_sales,
        total_profit,
        profit_margin,
        total_orders,
        total_customers,
        total_products,
        total_quantity
    )


# ==================================================
# BUSINESS OVERVIEW
# ==================================================

def show_business_overview():

    st.title("📊 Business Overview")

    st.caption(
        "Monitor sales, profitability, customers and "
        "products using the selected filters."
    )


    if len(filtered_df) == 0:

        st.warning(
            "No data is available for the selected filters."
        )

        return


    # --------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------

    (
        total_sales,
        total_profit,
        profit_margin,
        total_orders,
        total_customers,
        total_products,
        total_quantity
    ) = calculate_kpis(filtered_df)


    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

    st.subheader("Key Performance Indicators")


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Sales",
        money(total_sales)
    )


    col2.metric(
        "Total Profit",
        money(total_profit)
    )


    col3.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )


    col4.metric(
        "Orders",
        number(total_orders)
    )


    col5, col6, col7 = st.columns(3)


    col5.metric(
        "Customers",
        number(total_customers)
    )


    col6.metric(
        "Products",
        number(total_products)
    )


    col7.metric(
        "Quantity Sold",
        number(total_quantity)
    )


    # --------------------------------------------------
    # MONTHLY SALES AND PROFIT
    # --------------------------------------------------

    st.subheader("Monthly Sales & Profit")


    monthly_data = (
        filtered_df
        .groupby(
            filtered_df["Order Date"].dt.to_period("M")
        )
        .agg({
            "Sales": "sum",
            "Profit": "sum"
        })
        .reset_index()
    )


    monthly_data["Order Date"] = (
        monthly_data["Order Date"].astype(str)
    )


    fig = px.line(
        monthly_data,
        x="Order Date",
        y=["Sales", "Profit"],
        markers=True,
        title="Monthly Sales and Profit"
    )


    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount",
        legend_title="Metric"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # YEARLY SALES
    # --------------------------------------------------

    st.subheader("Yearly Sales")


    yearly_sales = (
        filtered_df
        .groupby(
            filtered_df["Order Date"].dt.year
        )["Sales"]
        .sum()
        .reset_index()
    )


    yearly_sales.columns = [
        "Year",
        "Sales"
    ]


    fig = px.bar(
        yearly_sales,
        x="Year",
        y="Sales",
        text_auto=".2s",
        title="Yearly Sales"
    )


    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Sales"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==================================================
# SALES ANALYSIS
# ==================================================

def show_sales_analysis():

    st.title("💰 Sales Analysis")

    st.caption(
        "Explore sales performance across categories, "
        "sub-categories, regions, segments and time."
    )


    if len(filtered_df) == 0:

        st.warning(
            "No data is available for the selected filters."
        )

        return


    # --------------------------------------------------
    # CATEGORY SALES
    # --------------------------------------------------

    st.subheader("Sales by Category")


    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )


    fig = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        text_auto=".2s",
        title="Sales by Category"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # SUB-CATEGORY SALES
    # --------------------------------------------------

    st.subheader("Sales by Sub-Category")


    subcategory_sales = (
        filtered_df
        .groupby("Sub-Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )


    fig = px.bar(
        subcategory_sales,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Sales by Sub-Category"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # REGION AND SEGMENT
    # --------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("Sales by Region")


        region_sales = (
            filtered_df
            .groupby("Region")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )


        fig = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            title="Regional Sales"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


    with col2:

        st.subheader("Sales by Segment")


        segment_sales = (
            filtered_df
            .groupby("Segment")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )


        fig = px.bar(
            segment_sales,
            x="Segment",
            y="Sales",
            title="Segment Sales"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


    # --------------------------------------------------
    # DISCOUNT VS PROFIT
    # --------------------------------------------------

    st.subheader("Discount vs Profit")


    st.caption(
        "This view shows the association between "
        "discount levels and total profit."
    )


    discount_profit = (
        filtered_df
        .groupby("Discount")["Profit"]
        .sum()
        .reset_index()
    )


    fig = px.line(
        discount_profit,
        x="Discount",
        y="Profit",
        markers=True,
        title="Discount vs Total Profit"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # MONTHLY SALES
    # --------------------------------------------------

    st.subheader("Monthly Sales")


    monthly_sales = (
        filtered_df
        .groupby(
            filtered_df["Order Date"].dt.month
        )["Sales"]
        .sum()
        .reset_index()
    )


    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]


    monthly_sales["Month"] = (
        monthly_sales["Order Date"]
        .apply(lambda x: month_names[x - 1])
    )


    fig = px.bar(
        monthly_sales,
        x="Month",
        y="Sales",
        title="Monthly Sales"
    )


    fig.update_xaxes(
        categoryorder="array",
        categoryarray=month_names
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


# ==================================================
# PRODUCT ANALYSIS
# ==================================================

def show_product_analysis():

    st.title("📦 Product Analysis")

    st.caption(
        "Identify the products and sub-categories "
        "that contribute the most to sales and profit."
    )


    if len(filtered_df) == 0:

        st.warning(
            "No data is available for the selected filters."
        )

        return


    # --------------------------------------------------
    # TOP 10 PRODUCTS BY SALES
    # --------------------------------------------------

    st.subheader("Top 10 Products by Sales")


    top_sales = (
        filtered_df
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )


    fig = px.bar(
        top_sales,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Sales"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # TOP 10 PRODUCTS BY PROFIT
    # --------------------------------------------------

    st.subheader("Top 10 Products by Profit")


    top_profit = (
        filtered_df
        .groupby("Product Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )


    fig = px.bar(
        top_profit,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Profit"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # BOTTOM 10 PRODUCTS
    # --------------------------------------------------

    st.subheader("⚠️ Bottom 10 Products by Profit")


    bottom_profit = (
        filtered_df
        .groupby("Product Name")["Profit"]
        .sum()
        .sort_values()
        .head(10)
        .reset_index()
    )


    fig = px.bar(
        bottom_profit,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Bottom 10 Products by Profit"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # SUB-CATEGORY PERFORMANCE
    # --------------------------------------------------

    st.subheader("Sub-Category Performance")


    subcategory_performance = (
        filtered_df
        .groupby("Sub-Category")
        .agg({
            "Sales": "sum",
            "Profit": "sum"
        })
        .reset_index()
        .sort_values("Profit", ascending=False)
    )


    st.dataframe(
        subcategory_performance.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}"
        }),
        width="stretch"
    )


    # --------------------------------------------------
    # LOSS-MAKING SUB-CATEGORIES
    # --------------------------------------------------

    st.subheader("⚠️ Loss-Making Sub-Categories")


    loss_subcategories = (
        subcategory_performance[
            subcategory_performance["Profit"] < 0
        ]
        .sort_values("Profit")
    )


    if len(loss_subcategories) > 0:

        st.dataframe(
            loss_subcategories.style.format({
                "Sales": "${:,.2f}",
                "Profit": "${:,.2f}"
            }),
            width="stretch"
        )

    else:

        st.success(
            "No loss-making sub-categories "
            "for the current filters."
        )


# ==================================================
# REGIONAL & CUSTOMER ANALYSIS
# ==================================================

def show_regional_customer_analysis():

    st.title("🌍 Regional & Customer Analysis")

    st.caption(
        "Analyze regional performance, customer segments "
        "and high-value customers."
    )


    if len(filtered_df) == 0:

        st.warning(
            "No data is available for the selected filters."
        )

        return


    # --------------------------------------------------
    # REGIONAL PERFORMANCE
    # --------------------------------------------------

    st.subheader("Regional Performance")


    region_performance = (
        filtered_df
        .groupby("Region")
        .agg({
            "Sales": "sum",
            "Profit": "sum"
        })
        .reset_index()
        .sort_values("Sales", ascending=False)
    )


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            region_performance,
            x="Region",
            y="Sales",
            title="Sales by Region"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


    with col2:

        fig = px.bar(
            region_performance,
            x="Region",
            y="Profit",
            title="Profit by Region"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


    # --------------------------------------------------
    # REGIONAL TABLE
    # --------------------------------------------------

    st.dataframe(
        region_performance.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}"
        }),
        width="stretch"
    )


    # --------------------------------------------------
    # REGION × CATEGORY
    # --------------------------------------------------

    st.subheader("Region × Category Sales")


    region_category = (
        filtered_df
        .pivot_table(
            index="Region",
            columns="Category",
            values="Sales",
            aggfunc="sum"
        )
        .fillna(0)
    )


    st.dataframe(
        region_category.style.format("${:,.2f}"),
        width="stretch"
    )


    # --------------------------------------------------
    # CUSTOMER SEGMENTS
    # --------------------------------------------------

    st.subheader("Customer Segment Performance")


    segment_performance = (
        filtered_df
        .groupby("Segment")
        .agg({
            "Sales": "sum",
            "Profit": "sum"
        })
        .reset_index()
        .sort_values("Sales", ascending=False)
    )


    fig = px.bar(
        segment_performance,
        x="Segment",
        y="Sales",
        title="Sales by Customer Segment"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    st.dataframe(
        segment_performance.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}"
        }),
        width="stretch"
    )


    # --------------------------------------------------
    # TOP CUSTOMERS
    # --------------------------------------------------

    st.subheader("Top 10 Customers by Sales")


    top_customers = (
        filtered_df
        .groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
        .reset_index()
    )


    fig = px.bar(
        top_customers,
        x="Sales",
        y="Customer Name",
        orientation="h",
        title="Top 10 Customers"
    )


    st.plotly_chart(
        fig,
        width="stretch"
    )


    # --------------------------------------------------
    # STRONGEST REGION
    # --------------------------------------------------

    strongest_region = (
        region_performance
        .sort_values("Sales", ascending=False)
        .iloc[0]
    )


    st.success(
        f"🏆 **Strongest Region:** "
        f"{strongest_region['Region']} "
        f"with {money(strongest_region['Sales'])} in sales."
    )


# ==================================================
# SALES FORECAST
# ==================================================

def show_sales_forecast():

    st.title("🔮 Sales Forecast")

    st.caption(
        "Future sales predictions generated from "
        "the forecasting stage of the project."
    )


    try:

        forecast_df = load_forecast()

    except FileNotFoundError:

        st.error(
            "future_sales_forecast.csv was not found. "
            "Please check data/processed/."
        )

        return


    # --------------------------------------------------
    # FORECAST DATA
    # --------------------------------------------------

    st.subheader("Forecast Data")


    st.dataframe(
        forecast_df,
        width="stretch"
    )


    # --------------------------------------------------
    # FIND FORECAST COLUMNS
    # --------------------------------------------------

    date_column = None
    forecast_column = None


    for column in forecast_df.columns:

        if "date" in column.lower():

            date_column = column


        if "forecast" in column.lower():

            forecast_column = column


    # --------------------------------------------------
    # FORECAST KPIs
    # --------------------------------------------------

    if forecast_column is not None:

        average_forecast = (
            forecast_df[forecast_column].mean()
        )


        total_forecast = (
            forecast_df[forecast_column].sum()
        )


        col1, col2 = st.columns(2)


        col1.metric(
            "Average Monthly Forecast",
            money(average_forecast)
        )


        col2.metric(
            "12-Month Forecast",
            money(total_forecast)
        )


    else:

        st.warning(
            "Forecast column was not found."
        )


    # --------------------------------------------------
    # HISTORICAL VS FORECAST
    # --------------------------------------------------

    if (
        date_column is not None
        and forecast_column is not None
    ):

        st.subheader(
            "Historical Sales vs Future Forecast"
        )


        historical_sales = (
            df
            .groupby(
                df["Order Date"].dt.to_period("M")
            )["Sales"]
            .sum()
            .reset_index()
        )


        historical_sales["Order Date"] = (
            historical_sales["Order Date"].astype(str)
        )


        historical_sales = historical_sales.rename(
            columns={
                "Sales": "Historical Sales"
            }
        )


        future_sales = forecast_df[
            [date_column, forecast_column]
        ].copy()


        future_sales[date_column] = pd.to_datetime(
            future_sales[date_column]
        )


        future_sales[date_column] = (
            future_sales[date_column]
            .dt.to_period("M")
            .astype(str)
        )


        future_sales = future_sales.rename(
            columns={
                date_column: "Order Date",
                forecast_column: "Forecast Sales"
            }
        )


        combined_data = pd.merge(
            historical_sales,
            future_sales,
            on="Order Date",
            how="outer"
        )


        combined_data = combined_data.sort_values(
            "Order Date"
        )


        fig = px.line(
            combined_data,
            x="Order Date",
            y=[
                "Historical Sales",
                "Forecast Sales"
            ],
            markers=True,
            title="Historical Sales and Future Forecast"
        )


        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Sales"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


    else:

        st.warning(
            "The forecast file needs a date column "
            "and a forecast column."
        )


# ==================================================
# MODEL PERFORMANCE
# ==================================================

def show_model_performance():

    st.title("📊 Model Performance")

    st.caption(
        "Compare forecasting models using MAE, RMSE "
        "and MAPE. Lower values indicate better performance."
    )


    try:

        results = load_model_results()

    except FileNotFoundError:

        st.error(
            "model_evaluation_results.csv was not found. "
            "Please check data/processed/."
        )

        return


    # --------------------------------------------------
    # MODEL RESULTS
    # --------------------------------------------------

    st.subheader("Model Comparison")


    st.dataframe(
        results,
        width="stretch"
    )


    # --------------------------------------------------
    # FIND COLUMNS
    # --------------------------------------------------

    model_column = None
    mae_column = None
    rmse_column = None
    mape_column = None


    for column in results.columns:

        column_name = column.lower()


        if "model" in column_name:

            model_column = column


        elif "mae" in column_name:

            mae_column = column


        elif "rmse" in column_name:

            rmse_column = column


        elif "mape" in column_name:

            mape_column = column


    # --------------------------------------------------
    # BEST MODEL
    # --------------------------------------------------

    if (
        model_column is not None
        and mae_column is not None
    ):

        best_row = results.loc[
            results[mae_column].idxmin()
        ]


        best_model = best_row[model_column]


        st.success(
            f"🏆 **Best Model:** {best_model}"
        )


    # --------------------------------------------------
    # MAE
    # --------------------------------------------------

    if model_column is not None:

        if mae_column is not None:

            st.subheader("MAE Comparison")


            mae_data = (
                results[
                    [model_column, mae_column]
                ]
                .sort_values(mae_column)
            )


            fig = px.bar(
                mae_data,
                x=model_column,
                y=mae_column,
                title="Mean Absolute Error"
            )


            st.plotly_chart(
                fig,
                width="stretch"
            )


        # --------------------------------------------------
        # RMSE
        # --------------------------------------------------

        if rmse_column is not None:

            st.subheader("RMSE Comparison")


            rmse_data = (
                results[
                    [model_column, rmse_column]
                ]
                .sort_values(rmse_column)
            )


            fig = px.bar(
                rmse_data,
                x=model_column,
                y=rmse_column,
                title="Root Mean Squared Error"
            )


            st.plotly_chart(
                fig,
                width="stretch"
            )


        # --------------------------------------------------
        # MAPE
        # --------------------------------------------------

        if mape_column is not None:

            st.subheader("MAPE Comparison")


            mape_data = (
                results[
                    [model_column, mape_column]
                ]
                .sort_values(mape_column)
            )


            fig = px.bar(
                mape_data,
                x=model_column,
                y=mape_column,
                title="Mean Absolute Percentage Error"
            )


            st.plotly_chart(
                fig,
                width="stretch"
            )


# ==================================================
# BUSINESS RECOMMENDATIONS
# ==================================================

def show_recommendations():

    st.title("💡 Business Recommendations")

    st.caption(
        "Data-driven observations and recommendations "
        "based on the selected data."
    )


    if len(filtered_df) == 0:

        st.warning(
            "No data is available for the selected filters."
        )

        return


    # --------------------------------------------------
    # STRONGEST REGION
    # --------------------------------------------------

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
    )


    strongest_region = region_sales.idxmax()

    strongest_region_sales = region_sales.max()


    # --------------------------------------------------
    # MOST PROFITABLE CATEGORY
    # --------------------------------------------------

    category_profit = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
    )


    most_profitable_category = (
        category_profit.idxmax()
    )


    highest_category_profit = (
        category_profit.max()
    )


    # --------------------------------------------------
    # BEST SALES MONTH
    # --------------------------------------------------

    month_sales = (
        filtered_df
        .groupby(
            filtered_df["Order Date"].dt.month
        )["Sales"]
        .sum()
    )


    best_month_number = month_sales.idxmax()


    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]


    best_month = (
        month_names[best_month_number - 1]
    )


    # --------------------------------------------------
    # LOSS-MAKING SUB-CATEGORIES
    # --------------------------------------------------

    subcategory_profit = (
        filtered_df
        .groupby("Sub-Category")["Profit"]
        .sum()
    )


    loss_making = (
        subcategory_profit[
            subcategory_profit < 0
        ]
        .sort_values()
    )


    # --------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------

    st.subheader("🔎 Key Insights")


    st.info(
        f"🌍 **Strongest Region:** "
        f"{strongest_region} with "
        f"{money(strongest_region_sales)} in sales."
    )


    st.info(
        f"🏆 **Most Profitable Category:** "
        f"{most_profitable_category} with "
        f"{money(highest_category_profit)} in profit."
    )


    st.info(
        f"📅 **Highest Sales Month:** "
        f"{best_month}."
    )


    if len(loss_making) > 0:

        loss_names = ", ".join(
            loss_making.index.tolist()
        )


        st.warning(
            f"⚠️ **Loss-Making Sub-Categories:** "
            f"{loss_names}."
        )


    else:

        st.success(
            "No loss-making sub-categories "
            "for the current filters."
        )


    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader("📌 Recommendations")


    st.markdown(
        f"""
### 1. Focus on {strongest_region}

The {strongest_region} region currently generates
the highest sales. Continue monitoring demand,
customer activity and inventory requirements in
this region.


### 2. Support {most_profitable_category}

{most_profitable_category} is currently the most
profitable category. Maintain availability while
continuing to monitor demand and profitability.


### 3. Prepare for {best_month}

Sales are highest during {best_month} in the
current filtered data. This pattern can be used
for inventory and operational planning.


### 4. Review loss-making areas

Loss-making sub-categories should be investigated
for pricing, discounts, product costs and demand.


### 5. Monitor discount levels

The analysis shows an association between discount
levels and profitability. Discount policies should
therefore be monitored carefully.
"""
    )


# ==================================================
# POWER BI
# ==================================================

def show_power_bi():

    st.sidebar.divider()

    st.sidebar.subheader("📊 Power BI")


    if POWER_BI_URL != "":

        st.sidebar.markdown(
            f"[Open Power BI Dashboard]({POWER_BI_URL})"
        )

    else:

        st.sidebar.info(
            "Power BI dashboard link will be added here."
        )


# ==================================================
# POWER BI SIDEBAR
# ==================================================

show_power_bi()


# ==================================================
# PAGE NAVIGATION
# ==================================================

if page == "Business Overview":

    show_business_overview()


elif page == "Sales Analysis":

    show_sales_analysis()


elif page == "Product Analysis":

    show_product_analysis()


elif page == "Regional & Customer Analysis":

    show_regional_customer_analysis()


elif page == "Sales Forecast":

    show_sales_forecast()


elif page == "Model Performance":

    show_model_performance()


elif page == "Business Recommendations":

    show_recommendations()


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Sales Forecasting & Business Analytics Dashboard | "
    "Built with Python, Pandas, Plotly and Streamlit"
)