import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import warnings

# Streamlit app title
st.title("Sales and Profit Analysis Dashboard")

# Ignore warnings
warnings.filterwarnings("ignore")

# Load your data into `df_dummy`
# Replace this example with your actual data loading method (e.g., file upload)
st.sidebar.subheader("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Choose file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Data successfully loaded!")
else:
    st.warning("Please upload a dataset to proceed.")

if uploaded_file is not None:
    # Copy and clean data
    df_dummy = df.copy()

    # Cleaning columns to remove symbols and convert to numerical
    cols_to_clean = [
        "manufacturing_price($)",
        "sale_price($)",
        "gross_sales($)",
        "discounts($)",
        "sales($)",
        "cogs($)",
        "profit($)",
        "units_sold($)"
    ]
    for col in cols_to_clean:
        df_dummy[col] = (
            df_dummy[col]
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("-", "0", regex=False)
            .str.replace("(", "-", regex=False)
            .str.replace(")", "", regex=False)
            .str.strip()
        )
    df_dummy[cols_to_clean] = df_dummy[cols_to_clean].astype(float)
    df_dummy["date"] = pd.to_datetime(df_dummy["date"], errors="coerce")

    # Replace NaN in `profit($)` with the mean
    df_dummy["profit($)"] = df_dummy["profit($)"].fillna(df_dummy["profit($)"].mean())

    # Display the cleaned DataFrame
    st.subheader("Cleaned Dataset")
    st.write(df_dummy.head())

    # Descriptive statistics
    st.subheader("Descriptive Statistics")
    st.write(df_dummy.describe())

    # Numerical and Non-numerical column classification
    num_col = df_dummy.select_dtypes(include=["int64", "float64"]).columns
    non_num_col = df_dummy.select_dtypes(include=["object"]).columns
    st.subheader("Column Classification")
    st.write("Numerical Columns:", list(num_col))
    st.write("Non-Numerical Columns:", list(non_num_col))

    # Bar Chart: Sales by Product and Month
    st.subheader("Sales by Product and Month")
    sales_by_product_month = df_dummy.groupby(["product", "month_name"])["sales($)"].sum().unstack()
    fig1, ax1 = plt.subplots(figsize=(15, 8))
    sales_by_product_month.plot(kind="bar", ax=ax1)
    ax1.set_title("Sales by Product and Month")
    ax1.set_xlabel("Product")
    ax1.set_ylabel("Total Sales")
    ax1.legend(title="Month")
    ax1.tick_params(axis="x", rotation=45)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1e6:.1f}M"))
    st.pyplot(fig1)

    # Line Chart: Trend in Profitability Across Months
    st.subheader("Trend in Profitability Across Months")
    profit_by_month = df_dummy.groupby("month_name")["profit($)"].sum().sort_values(ascending=True)
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(profit_by_month.index, profit_by_month.values, marker="o")
    ax2.set_title("Trend in Profitability Across Months")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Total Profit ($)")
    ax2.tick_params(axis="x", rotation=45)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1e6:.1f}M"))
    ax2.grid(True)
    st.pyplot(fig2)

    # Bar Chart: Revenue Contribution by Product
    st.subheader("Revenue Contribution by Product")
    product_revenue = df_dummy.groupby("product")["sales($)"].sum().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    product_revenue.plot(kind="bar", ax=ax3)
    ax3.set_title("Revenue Contribution by Product")
    ax3.set_xlabel("Product")
    ax3.set_ylabel("Total Revenue ($)")
    ax3.tick_params(axis="x", rotation=45)
    ax3.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x / 1e6:.1f}M"))
    st.pyplot(fig3)

    # Pie Chart: Revenue Distribution by Product
    st.subheader("Revenue Distribution by Product")
    fig4, ax4 = plt.subplots(figsize=(8, 8))
    ax4.pie(product_revenue, labels=product_revenue.index, autopct="%1.1f%%", startangle=90)
    ax4.set_title("Revenue Distribution by Product")
    st.pyplot(fig4)

    # Line Chart: Trend in Unit Sales Across Months
    st.subheader("Trend in Unit Sales Across Months")
    units_sold_by_month = df_dummy.groupby("month_name")["units_sold($)"].sum().sort_values(ascending=True)
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    ax5.plot(units_sold_by_month.index, units_sold_by_month.values, marker="o")
    ax5.set_title("Trend in Unit Sales Across Months")
    ax5.set_xlabel("Month")
    ax5.set_ylabel("Total Units Sold")
    ax5.tick_params(axis="x", rotation=45)
    ax5.grid(True)
    st.pyplot(fig5)

    # Streamlit App
    st.title("Sales and Profit Analysis")

    # Group data by product and calculate total sales and profit
    product_performance = df_dummy.groupby('product').agg({'sales($)': 'sum', 'profit($)': 'sum'})

    # Sort products by sales in descending order
    product_performance = product_performance.sort_values('sales($)', ascending=False)

    # Create a bar chart comparing sales and profit across products
    st.subheader("Product Performance: Sales and Profit")
    fig1, ax1 = plt.subplots(figsize=(15, 8))
    product_performance[['sales($)', 'profit($)']].plot(kind='bar', ax=ax1)
    ax1.set_title('Product Performance: Sales and Profit')
    ax1.set_xlabel('Product')
    ax1.set_ylabel('Total Sales/Profit ($)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(['Sales', 'Profit'])
    # Format the y-axis in millions
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x / 1e6:.1f}M'))
    st.pyplot(fig1)

    # Create a dataframe showing sales and profit for each product
    sales_profit_df = pd.DataFrame({
        'Product': product_performance.index,
        'Total Sales': product_performance['sales($)'],
        'Total Profit': product_performance['profit($)']
    })

    st.write(sales_profit_df)

    # "How does sales performance vary across different segments?"
    st.subheader("Sales Trend Across Months by Segment")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    for segment in df_dummy['segment'].unique():
        sales_segment_month = df_dummy[df_dummy['segment'] == segment].groupby('month_name')['sales($)'].sum()
        ax2.plot(sales_segment_month.index, sales_segment_month.values, label=segment)
    ax2.set_title('Sales Trend Across Months by Segment')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Total Sales ($)')
    ax2.tick_params(axis='x', rotation=45)
    # Format the y-axis in millions
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x / 1e6:.1f}M'))
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

    # "Which segment contributes the most to the overall revenue?"
    st.subheader("Revenue Contribution by Segment")
    segment_revenue = df_dummy.groupby('segment')['sales($)'].sum()
    segment_revenue = segment_revenue.sort_values(ascending=False)

    # Create a bar chart showing the distribution of revenue across different segments
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    segment_revenue.plot(kind='bar', ax=ax3)
    ax3.set_title('Revenue Contribution by Segment')
    ax3.set_xlabel('Segment')
    ax3.set_ylabel('Total Revenue ($)')
    ax3.tick_params(axis='x', rotation=45)
    # Format the y-axis in millions
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x / 1e6:.1f}M'))
    st.pyplot(fig3)

    # Alternatively, pie chart for revenue distribution by segment
    st.subheader("Revenue Distribution by Segment")
    fig4, ax4 = plt.subplots(figsize=(8, 8))
    ax4.pie(segment_revenue, labels=segment_revenue.index, autopct='%1.1f%%', startangle=45)
    ax4.set_title('Revenue Distribution by Segment')
    st.pyplot(fig4)

    # "How does the profit margin compare across different segments?"
    st.subheader("Profit Margin Comparison Across Segments")
    segment_profit_margin = df_dummy.groupby('segment').apply(
        lambda x: (x['profit($)'].sum() / x['sales($)'].sum()) * 100 if x['sales($)'].sum() > 0 else 0
    )
    segment_profit_margin.sort_values(ascending=False, inplace=True)

    # Create a bar chart comparing profit margins across different segments
    fig5, ax5 = plt.subplots(figsize=(12, 6))
    segment_profit_margin.plot(kind='bar', ax=ax5)
    ax5.set_title('Profit Margin Comparison Across Segments')
    ax5.set_xlabel('Segment')
    ax5.set_ylabel('Profit Margin (%)')
    ax5.tick_params(axis='x', rotation=45)
    st.pyplot(fig5)


    # Streamlit App
    st.title("Discount Impact and Regional Sales Analysis")

    # "What is the impact of different discount bands on sales and profitability?"
    st.subheader("Impact of Discount Bands on Sales and Profitability")
    discount_impact = df_dummy.groupby('discount_band').agg({'sales($)': 'sum', 'profit($)': 'sum'})

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    discount_impact[['sales($)', 'profit($)']].plot(kind='bar', ax=ax1)
    ax1.set_title('Impact of Discount Bands on Sales and Profitability')
    ax1.set_xlabel('Discount Band')
    ax1.set_ylabel('Total Sales/Profit ($)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(['Sales', 'Profit'])
    # Format the y-axis in millions
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x / 1e6:.1f}M'))
    st.pyplot(fig1)

    # "Are there certain months or products where discounts are more effective?"
    st.subheader("Discount Effectiveness by Product and Month")
    discount_effectiveness = df_dummy.groupby(['discount_band', 'product', 'month_name'])['sales($)'].sum().reset_index()
    discount_effectiveness_pivot = discount_effectiveness.pivot_table(
        index=['discount_band', 'product'], columns='month_name', values='sales($)'
    ).fillna(0)

    fig2, ax2 = plt.subplots(figsize=(16, 10))
    sns.heatmap(discount_effectiveness_pivot, annot=True, fmt=".0f", cmap='viridis', ax=ax2)
    ax2.set_title('Discount Effectiveness by Product and Month')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Discount Band & Product')
    st.pyplot(fig2)

    # "How does the sales performance compare across countries?"
    st.subheader("Sales Performance Comparison Across Countries")
    country_sales = df_dummy.groupby('country')['sales($)'].sum()
    country_sales = country_sales.sort_values(ascending=False)

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    country_sales.plot(kind='bar', ax=ax3)
    ax3.set_title('Sales Performance Comparison Across Countries')
    ax3.set_xlabel('Country')
    ax3.set_ylabel('Total Sales ($)')
    ax3.tick_params(axis='x', rotation=45)
    # Format the y-axis in millions
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x / 1e6:.1f}M'))
    st.pyplot(fig3)

    # "Are there any specific countries that are driving significant profits?"
    st.subheader("Profitability Comparison Across Countries")
    country_profit = df_dummy.groupby('country')['profit($)'].sum()
    country_profit = country_profit.sort_values(ascending=False)

    fig4, ax4 = plt.subplots(figsize=(12, 6))
    country_profit.plot(kind='bar', ax=ax4)
    ax4.set_title('Profitability Comparison Across Countries')
    ax4.set_xlabel('Country')
    ax4.set_ylabel('Total Profit ($)')
    ax4.tick_params(axis='x', rotation=45)
    # Format the y-axis in millions
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x / 1e6:.1f}M'))
    st.pyplot(fig4)





