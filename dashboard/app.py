import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Ecommerce Sales Analytics",
    page_icon="🛒",
    layout="wide"
)


# =====================================================
# PROJECT PATH
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_ecommerce_sales.csv"
)


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"]
    )

    return df


df = load_data()


# =====================================================
# DASHBOARD HEADER
# =====================================================

st.title("🛒 Ecommerce Sales Analytics")

st.markdown(
    """
    **Sales, profitability, customer and operational performance dashboard**
    """
)


st.divider()


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Dashboard Filters")


# Year Filter
years = sorted(
    df["Year"].dropna().unique()
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + years
)


# Region Filter
regions = sorted(
    df["Region"].dropna().unique()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + regions
)


# Category Filter
categories = sorted(
    df["Category"].dropna().unique()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + categories
)


# Order Status Filter
statuses = sorted(
    df["Order_Status"].dropna().unique()
)

selected_status = st.sidebar.selectbox(
    "Select Order Status",
    ["All"] + statuses
)


# =====================================================
# APPLY FILTERS
# =====================================================

filtered_df = df.copy()


if selected_year != "All":

    filtered_df = filtered_df[
        filtered_df["Year"] == selected_year
    ]


if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


if selected_category != "All":

    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


if selected_status != "All":

    filtered_df = filtered_df[
        filtered_df["Order_Status"] == selected_status
    ]


# Add Filter Information
st.caption(
    f"Showing {len(filtered_df):,} records"
)


# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = filtered_df["Net_Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order_ID"].nunique()

total_customers = filtered_df["Customer_ID"].nunique()

total_units = filtered_df["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue > 0
    else 0
)


# =====================================================
# OPERATIONAL KPIs
# =====================================================

return_orders = filtered_df[
    filtered_df["Order_Status"] == "Returned"
]["Order_ID"].nunique()

cancelled_orders = filtered_df[
    filtered_df["Order_Status"] == "Cancelled"
]["Order_ID"].nunique()

return_rate = (
    return_orders / total_orders * 100
    if total_orders > 0
    else 0
)

cancellation_rate = (
    cancelled_orders / total_orders * 100
    if total_orders > 0
    else 0
)

total_shipping_cost = (
    filtered_df["Shipping_Cost"].sum()
)


# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )


with col2:

    st.metric(
        "Total Profit",
        f"₹{total_profit:,.0f}"
    )


with col3:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with col4:

    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

col5, col6, col7 = st.columns(3)

with col5:

    st.metric(
        "Units Sold",
        f"{total_units:,}"
    )


with col6:

    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.0f}"
    )


with col7:

    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )



# Add the New KPI Cards
st.divider()

col8, col9, col10 = st.columns(3)

with col8:

    st.metric(
        "Return Rate",
        f"{return_rate:.2f}%"
    )

with col9:

    st.metric(
        "Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )

with col10:

    st.metric(
        "Shipping Cost",
        f"₹{total_shipping_cost:,.0f}"
    )


# Add a Section Heading
st.divider()

st.header("📈 Sales Performance")


# Monthly Revenue Chart
monthly_sales = (
    filtered_df
    .groupby(
        ["Year", "Month", "Month_Name"],
        as_index=False
    )
    .agg(
        Revenue=("Net_Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values(
        ["Year", "Month"]
    )
)


# =====================================================
# MONTHLY REVENUE & PROFIT
# =====================================================

fig, ax = plt.subplots(
    figsize=(12, 5)
)

ax.plot(
    monthly_sales["Month_Name"],
    monthly_sales["Revenue"],
    marker="o",
    label="Revenue"
)

ax.plot(
    monthly_sales["Month_Name"],
    monthly_sales["Profit"],
    marker="o",
    label="Profit"
)

ax.set_title(
    "Monthly Revenue vs Profit"
)

ax.set_xlabel(
    "Month"
)

ax.set_ylabel(
    "Amount (₹)"
)

ax.legend()

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)

ax.plot(
    monthly_sales["Month_Name"],
    monthly_sales["Revenue"],
    marker="o"
)

ax.set_title(
    "Monthly Revenue"
)

ax.set_xlabel(
    "Month"
)

ax.set_ylabel(
    "Revenue (₹)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)



# Add Monthly Profit
fig, ax = plt.subplots(
    figsize=(10, 5)
)

ax.plot(
    monthly_sales["Month_Name"],
    monthly_sales["Profit"],
    marker="o"
)

ax.set_title(
    "Monthly Profit"
)

ax.set_xlabel(
    "Month"
)

ax.set_ylabel(
    "Profit (₹)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)


# Category and Region Analysis
st.divider()

st.header("📊 Category & Regional Performance")
st.caption(
    "Compare revenue and profitability across product categories and geographic regions."
)

col1, col2 = st.columns(2)

with col1:

    category_sales = (
        filtered_df
        .groupby("Category")["Net_Sales"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    category_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Revenue by Category"
    )

    ax.set_xlabel(
        "Category"
    )

    ax.set_ylabel(
        "Revenue (₹)"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig)


# Regional Revenue
with col2:

    region_sales = (
        filtered_df
        .groupby("Region")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    region_sales.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Revenue by Region"
    )

    ax.set_xlabel(
        "Region"
    )

    ax.set_ylabel(
        "Revenue (₹)"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig)


# =====================================================
# CATEGORY PROFITABILITY TABLE
# =====================================================

category_profitability = (
    filtered_df
    .groupby("Category")
    .agg(
        Revenue=("Net_Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

category_profitability["Profit_Margin"] = (
    category_profitability["Profit"]
    / category_profitability["Revenue"]
    * 100
)

category_profitability = (
    category_profitability
    .sort_values(
        "Profit",
        ascending=False
    )
)

st.subheader("📋 Category Profitability")
st.caption(
    "Revenue, profit and profit margin by product category."
)

st.dataframe(
    category_profitability.style.format({
        "Revenue": "₹{:,.0f}",
        "Profit": "₹{:,.0f}",
        "Profit_Margin": "{:.2f}%"
    }),
    use_container_width=True
)


# =====================================================
# TOP PRODUCTS TABLE
# =====================================================

top_product_table = (
    filtered_df
    .groupby("Product")
    .agg(
        Revenue=("Net_Sales", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    )
    .reset_index()
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)

st.subheader("🏆 Top 10 Products")
st.caption(
    "Products ranked by revenue contribution within the current filter selection."
)

st.dataframe(
    top_product_table.style.format({
        "Revenue": "₹{:,.0f}",
        "Profit": "₹{:,.0f}",
        "Units_Sold": "{:,.0f}"
    }),
    use_container_width=True
)


# =====================================================
# REGIONAL PROFITABILITY
# =====================================================

regional_profit = (
    filtered_df
    .groupby("Region")["Profit"]
    .sum()
    .sort_values(
        ascending=False
    )
)

fig, ax = plt.subplots(
    figsize=(10, 5)
)

regional_profit.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Profit by Region"
)

ax.set_xlabel(
    "Region"
)

ax.set_ylabel(
    "Profit (₹)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)


# Top 10 Products
st.divider()

st.header("🏆 Top Products")

top_products = (
    filtered_df
    .groupby("Product")["Net_Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

fig, ax = plt.subplots(
    figsize=(10, 5)
)

top_products.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_title(
    "Top 10 Products by Revenue"
)

ax.set_xlabel(
    "Revenue (₹)"
)

ax.set_ylabel(
    "Product"
)

plt.tight_layout()

st.pyplot(fig)

st.divider()


# =====================================================
# CUSTOMER PERFORMANCE
# =====================================================

st.header("👥 Customer Performance")

customer_performance = (
    filtered_df
    .groupby("Customer_ID")
    .agg(
        Orders=("Order_ID", "nunique"),
        Revenue=("Net_Sales", "sum"),
        Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    )
    .reset_index()
    .sort_values(
        "Revenue",
        ascending=False
    )
)

st.subheader("🏆 Top Customers by Revenue")

st.dataframe(
    customer_performance.head(10).style.format({
        "Revenue": "₹{:,.0f}",
        "Profit": "₹{:,.0f}",
        "Units_Sold": "{:,.0f}"
    }),
    use_container_width=True
)


# =====================================================
# CUSTOMER REVENUE CHART
# =====================================================

top_customers = (
    customer_performance
    .head(10)
    .sort_values("Revenue")
)

fig, ax = plt.subplots(
    figsize=(10, 5)
)

top_customers.plot(
    x="Customer_ID",
    y="Revenue",
    kind="barh",
    ax=ax,
    legend=False
)

ax.set_title(
    "Top 10 Customers by Revenue"
)

ax.set_xlabel(
    "Revenue (₹)"
)

ax.set_ylabel(
    "Customer"
)

plt.tight_layout()

st.pyplot(fig)

st.divider()


# =====================================================
# CUSTOMER SEGMENTATION
# =====================================================

st.subheader("👥 Customer Segmentation")
st.caption(
    "Customer segments based on revenue and profitability contribution."
)

customer_segments = (
    customer_performance
    .copy()
)

customer_segments["Customer_Segment"] = pd.cut(
    customer_segments["Revenue"],
    bins=[
        -float("inf"),
        50000,
        150000,
        300000,
        float("inf")
    ],
    labels=[
        "Low Value",
        "Medium Value",
        "High Value",
        "VIP"
    ]
)

segment_summary = (
    customer_segments
    .groupby("Customer_Segment", observed=False)
    .agg(
        Customers=("Customer_ID", "nunique"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

st.dataframe(
    segment_summary.style.format({
        "Revenue": "₹{:,.0f}",
        "Profit": "₹{:,.0f}"
    }),
    use_container_width=True
)

segment_revenue = (
    segment_summary
    .set_index("Customer_Segment")["Revenue"]
)

fig, ax = plt.subplots(
    figsize=(10, 5)
)

segment_revenue.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Revenue by Customer Segment"
)

ax.set_xlabel(
    "Customer Segment"
)

ax.set_ylabel(
    "Revenue (₹)"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

st.pyplot(fig)

st.divider()


# =====================================================
# REPEAT CUSTOMER ANALYSIS
# =====================================================

st.subheader("🔁 Repeat Customer Analysis")
st.caption(
    "Identifies repeat customers and highlights their purchase contribution."
)

repeat_customers = (
    customer_performance[
        customer_performance["Orders"] > 1
    ]
    .sort_values(
        "Orders",
        ascending=False
    )
)

total_customers = customer_performance["Customer_ID"].nunique()

repeat_customer_count = repeat_customers["Customer_ID"].nunique()

repeat_customer_rate = (
    repeat_customer_count
    / total_customers
    * 100
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Repeat Customers",
        repeat_customer_count
    )

with col2:
    st.metric(
        "Repeat Customer Rate",
        f"{repeat_customer_rate:.2f}%"
    )

st.dataframe(
    repeat_customers.head(10).style.format({
        "Revenue": "₹{:,.0f}",
        "Profit": "₹{:,.0f}",
        "Units_Sold": "{:,.0f}"
    }),
    use_container_width=True
)


# =====================================================
# REPEAT CUSTOMER ORDERS
# =====================================================

fig, ax = plt.subplots(
    figsize=(10, 5)
)

repeat_customers.head(10).plot(
    x="Customer_ID",
    y="Orders",
    kind="bar",
    ax=ax,
    legend=False
)

ax.set_title(
    "Top Repeat Customers by Number of Orders"
)

ax.set_xlabel(
    "Customer"
)

ax.set_ylabel(
    "Number of Orders"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)


# Order Status Analysis
st.divider()

st.header("📦 Order Status")

status_counts = (
    filtered_df
    .groupby("Order_Status")["Order_ID"]
    .nunique()
    .sort_values(
        ascending=False
    )
)

fig, ax = plt.subplots(
    figsize=(8, 5)
)

status_counts.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Orders by Status"
)

ax.set_xlabel(
    "Order Status"
)

ax.set_ylabel(
    "Number of Orders"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

st.pyplot(fig)

st.divider()


# =====================================================
# EXECUTIVE INSIGHTS & RECOMMENDATIONS
# =====================================================

st.header("📊 Executive Insights & Recommendations")
st.caption(
    "Key business findings and recommended actions based on the selected filters."
)

# =====================================================
# MONTHLY PERFORMANCE
# =====================================================

# Aggregate monthly revenue and profit
monthly_performance = (
    filtered_df
    .groupby("Month", as_index=True)
    .agg(
        Revenue=("Net_Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

# -----------------------------------------------------
# Ensure all 12 months are present and correctly ordered
# -----------------------------------------------------

month_order = list(range(1, 13))

monthly_performance = (
    monthly_performance
    .reindex(month_order)
    .fillna(0)
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

monthly_performance["Month_Name"] = month_names

# Keep numeric month for sorting
monthly_performance["Month_Number"] = month_order

# -----------------------------------------------------
# Best / Worst Months
# -----------------------------------------------------

best_revenue_month = (
    monthly_performance.loc[
        monthly_performance["Revenue"].idxmax(),
        "Month_Name"
    ]
)

best_revenue_value = (
    monthly_performance["Revenue"].max()
)

best_profit_month = (
    monthly_performance.loc[
        monthly_performance["Profit"].idxmax(),
        "Month_Name"
    ]
)

best_profit_value = (
    monthly_performance["Profit"].max()
)

worst_profit_month = (
    monthly_performance.loc[
        monthly_performance["Profit"].idxmin(),
        "Month_Name"
    ]
)

worst_profit_value = (
    monthly_performance["Profit"].min()
)


# =====================================================
# MONTHLY KPI SUMMARY
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Best Revenue Month",
        best_revenue_month,
        f"₹{best_revenue_value:,.0f}"
    )

with col2:
    st.metric(
        "Best Profit Month",
        best_profit_month,
        f"₹{best_profit_value:,.0f}"
    )

with col3:
    st.metric(
        "Lowest Profit Month",
        worst_profit_month,
        f"₹{worst_profit_value:,.0f}"
    )


# =====================================================
# MANAGEMENT RECOMMENDATIONS
# =====================================================

st.subheader("💡 Management Recommendations")
st.caption(
    "Recommended actions derived from revenue, profitability and customer behavior."
)

st.markdown(
    f"""
### 1. 📈 Focus on High-Performing Months

**{best_revenue_month}** generated the highest revenue of
**₹{best_revenue_value:,.0f}**.

Increase inventory readiness, promotional activity and marketing
investment around historically strong periods.

### 2. 💰 Maximize Profitability

**{best_profit_month}** generated the highest profit of
**₹{best_profit_value:,.0f}**.

Prioritize products and categories that combine strong sales volume
with healthy margins.

### 3. ⚠️ Investigate Low-Profit Periods

**{worst_profit_month}** recorded the lowest profit of
**₹{worst_profit_value:,.0f}**.

Review discounts, product costs, pricing and shipping expenses during
lower-performing periods.

### 4. 👥 Retain High-Value Customers

Use the **High Value** and **VIP** customer segments to create
targeted loyalty offers and personalized campaigns.

### 5. 🔁 Increase Repeat Purchases

Use repeat-customer behavior to encourage additional purchases through
personalized recommendations, cross-selling and follow-up campaigns.
"""
)


# =====================================================
# MONTHLY PERFORMANCE TABLE
# =====================================================

st.subheader("📅 Monthly Performance")
st.caption(
    "Monthly revenue, profit and profit-margin performance for the current filter selection."
)

monthly_display = monthly_performance[
    ["Month_Name", "Revenue", "Profit"]
].copy()

monthly_display.columns = [
    "Month",
    "Revenue",
    "Profit"
]

# Calculate profit margin safely
monthly_display["Profit_Margin"] = (
    monthly_display["Profit"]
    .div(monthly_display["Revenue"].replace(0, float("nan")))
    .mul(100)
)

st.dataframe(
    monthly_display.style.format({
        "Revenue": "₹{:,.0f}",
        "Profit": "₹{:,.0f}",
        "Profit_Margin": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
st.caption(
    "Monthly revenue, profit and profit-margin performance for the current filter selection."
)


# =====================================================
# MONTHLY REVENUE VS PROFIT CHART
# =====================================================

st.subheader("📈 Monthly Revenue vs Profit")

fig_monthly, ax_monthly = plt.subplots(figsize=(12, 5))

ax_monthly.plot(
    monthly_display["Month"],
    monthly_display["Revenue"],
    marker="o",
    linewidth=2,
    label="Revenue"
)

ax_monthly.plot(
    monthly_display["Month"],
    monthly_display["Profit"],
    marker="o",
    linewidth=2,
    label="Profit"
)

ax_monthly.set_title("Monthly Revenue vs Profit")
ax_monthly.set_xlabel("Month")
ax_monthly.set_ylabel("Amount (₹)")

ax_monthly.tick_params(axis="x", rotation=45)

ax_monthly.legend()

ax_monthly.grid(
    axis="y",
    alpha=0.2
)

plt.tight_layout()

st.pyplot(
    fig_monthly,
    use_container_width=True
)

plt.close(fig_monthly)


# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.divider()

st.header("💡 Business Insights")

top_category = (
    filtered_df
    .groupby("Category")["Net_Sales"]
    .sum()
    .idxmax()
)

top_category_revenue = (
    filtered_df
    .groupby("Category")["Net_Sales"]
    .sum()
    .max()
)

top_region = (
    filtered_df
    .groupby("Region")["Net_Sales"]
    .sum()
    .idxmax()
)

top_product = (
    filtered_df
    .groupby("Product")["Net_Sales"]
    .sum()
    .idxmax()
)

top_product_revenue = (
    filtered_df
    .groupby("Product")["Net_Sales"]
    .sum()
    .max()
)

st.markdown(
    f"""
    ### 📌 Key Findings

    - **Top Revenue Category:** {top_category}
      with revenue of **₹{top_category_revenue:,.0f}**

    - **Top Revenue Region:** {top_region}

    - **Top Product:** {top_product}
      with revenue of **₹{top_product_revenue:,.0f}**

    - **Overall Profit Margin:** {profit_margin:.2f}%

    - **Return Rate:** {return_rate:.2f}%

    - **Cancellation Rate:** {cancellation_rate:.2f}%
    """
)


# Add Data Table
st.divider()

st.markdown(
    "<div style='margin-top: -10px;'></div>",
    unsafe_allow_html=True
)

st.header("📋 Sales Data")
st.caption("Detailed view of the currently filtered sales transactions.")

# Format Order Date
filtered_df["Order_Date"] = pd.to_datetime(
    filtered_df["Order_Date"]
).dt.strftime("%d %b %Y")

# Display table
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    height=520,
    column_config={
        "Order_ID": st.column_config.TextColumn(
            "Order ID",
            width="medium"
        ),
        "Order_Date": st.column_config.TextColumn(
            "Order Date",
            width="small"
        ),
        "Customer_ID": st.column_config.TextColumn(
            "Customer ID",
            width="small"
        ),
        "Product": st.column_config.TextColumn(
            "Product",
            width="medium"
        ),
        "Category": st.column_config.TextColumn(
            "Category",
            width="medium"
        ),
        "Quantity": st.column_config.NumberColumn(
            "Quantity",
            width="small"
        ),
        "Unit_Price": st.column_config.NumberColumn(
            "Unit Price",
            format="₹%,.0f",
            width="small"
        ),
        "Product_Cost": st.column_config.NumberColumn(
            "Product Cost",
            format="₹%,.0f",
            width="medium"
        ),
        "Discount": st.column_config.NumberColumn(
            "Discount",
            format="%.0f%%",
            width="small"
        ),
        "Revenue": st.column_config.NumberColumn(
            "Revenue",
            format="₹%,.0f",
            width="small"
        ),
        "Profit": st.column_config.NumberColumn(
            "Profit",
            format="₹%,.0f",
            width="small"
        ),
        "Payment_Method": st.column_config.TextColumn(
            "Payment Method",
            width="medium"
        ),
        "Region": st.column_config.TextColumn(
            "Region",
            width="small"
        ),
        "City": st.column_config.TextColumn(
            "City",
            width="medium"
        ),
        "Order_Status": st.column_config.TextColumn(
            "Order Status",
            width="medium"
        ),
       "Shipping_Cost": st.column_config.NumberColumn(
           "Shipping Cost",
           format="₹%,.0f",
           width="medium"
        ),
        "Gross_Sales": st.column_config.NumberColumn(
           "Gross Sales",
            format="₹%,.0f",
            width="medium"
        ),
    }
)


# =====================================================
# DOWNLOAD FILTERED DATA
# =====================================================

csv_data = filtered_df.to_csv(
    index=False
)

st.caption(
    "Download the currently filtered sales data as a CSV file."
)

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
    type="secondary"
)


# Add Footer
st.divider()

st.caption(
    "Ecommerce Sales Analytics | "
    "Built with Python, Pandas, SQL, SQLite and Streamlit"
)
