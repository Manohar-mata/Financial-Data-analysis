# finance_streamlit.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configure Streamlit page
st.set_page_config(page_title="Financial Data Analysis", layout="wide")

# Load the dataset
st.title("Financial Data Analysis")
st.sidebar.header("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file)

    # Cleaning column names
    df.rename(columns={
        'Segment': 'segment',
        'Country': 'country',
        ' Product ': 'product',
        ' Discount Band ': 'discount_band',
        ' Units Sold ': 'units_sold($)',
        ' Manufacturing Price ': 'manufacturing_price($)',
        ' Sale Price ': 'sale_price($)',
        ' Gross Sales ': 'gross_sales($)',
        ' Discounts ': 'discounts($)',
        '  Sales ': 'sales($)',
        ' COGS ': 'cogs($)',
        ' Profit ': 'profit($)',
        'Date': 'date',
        'Month Number': 'month_number',
        ' Month Name ': 'month_name',
        'Year': 'year'
    }, inplace=True)

    # Cleaning the dataset
    df.iloc[:, 4:12] = df.iloc[:, 4:12].apply(
        lambda x: x.str.replace(',', '')
                   .str.replace('(', '-')
                   .str.replace(')', '')
                   .str.strip()
                   .replace('-', np.nan)
                   .replace('', np.nan)
    )

    # Converting to numeric types
    for col in ['manufacturing_price($)', 'sale_price($)', 'gross_sales($)', 'discounts($)', 'sales($)', 'cogs($)', 'profit($)', 'units_sold($)']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill NaN in profit with mean
    df['profit($)'].fillna(df['profit($)'].mean(), inplace=True)

    # Data overview
    st.header("Dataset Overview")
    st.write("Shape of the dataset:", df.shape)
    st.write("First few rows of the dataset:")
    st.write(df.head())

    # Sidebar Filters
    st.sidebar.header("Filter Options")
    selected_segment = st.sidebar.multiselect("Select Segment(s)", df['segment'].unique())
    selected_product = st.sidebar.multiselect("Select Product(s)", df['product'].unique())
    filtered_df = df.copy()

    if selected_segment:
        filtered_df = filtered_df[filtered_df['segment'].isin(selected_segment)]
    if selected_product:
        filtered_df = filtered_df[filtered_df['product'].isin(selected_product)]

    st.write("Filtered Dataset:")
    st.write(filtered_df)

    # Overall Performance Analysis
    st.header("Overall Performance and Trends")
    if st.checkbox("Show Sales by Product and Month"):
        sales_by_product_month = filtered_df.groupby(['product', 'month_name'])['sales($)'].sum().unstack()
        fig, ax = plt.subplots(figsize=(15, 8))
        sales_by_product_month.plot(kind='bar', ax=ax)
        ax.set_title("Sales by Product and Month")
        ax.set_xlabel("Product")
        ax.set_ylabel("Total Sales")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    if st.checkbox("Show Profitability Trends Across Months"):
        profit_by_month = filtered_df.groupby('month_name')['profit($)'].sum()
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(profit_by_month.index, profit_by_month.values, marker='o')
        ax.set_title("Profitability Trends Across Months")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Profit")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    # Product-Specific Insights
    st.header("Product-Specific Insights")
    if st.checkbox("Show Product Sales and Profit"):
        product_performance = filtered_df.groupby('product').agg({'sales($)': 'sum', 'profit($)': 'sum'})
        product_performance = product_performance.sort_values('sales($)', ascending=False)
        fig, ax = plt.subplots(figsize=(15, 8))
        product_performance[['sales($)', 'profit($)']].plot(kind='bar', ax=ax)
        ax.set_title("Product Performance: Sales and Profit")
        ax.set_xlabel("Product")
        ax.set_ylabel("Total Sales/Profit")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    # Segmentation Analysis
    st.header("Segmentation Analysis")
    if st.checkbox("Show Revenue Contribution by Segment"):
        segment_revenue = filtered_df.groupby('segment')['sales($)'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(12, 6))
        segment_revenue.plot(kind='bar', ax=ax)
        ax.set_title("Revenue Contribution by Segment")
        ax.set_xlabel("Segment")
        ax.set_ylabel("Total Revenue")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    if st.checkbox("Show Profit Margin by Segment"):
        segment_profit_margin = filtered_df.groupby('segment').apply(
            lambda x: (x['profit($)'].sum() / x['sales($)'].sum()) * 100 if x['sales($)'].sum() > 0 else 0)
        fig, ax = plt.subplots(figsize=(12, 6))
        segment_profit_margin.plot(kind='bar', ax=ax)
        ax.set_title("Profit Margin by Segment")
        ax.set_xlabel("Segment")
        ax.set_ylabel("Profit Margin (%)")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    # Detailed Financial Analysis
    st.header("Detailed Financial Analysis")
    if st.checkbox("Show Product-Specific Sales Distribution"):
        fig, ax = plt.subplots(figsize=(15, 8))
        sns.boxplot(data=filtered_df, x='product', y='sales($)', ax=ax)
        ax.set_title("Sales Distribution by Product")
        ax.set_xlabel("Product")
        ax.set_ylabel("Sales")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    if st.checkbox("Show Discount Impact on Profit"):
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(data=filtered_df, x='discounts($)', y='profit($)', hue='segment', ax=ax)
        ax.set_title("Discounts vs Profit by Segment")
        ax.set_xlabel("Discounts")
        ax.set_ylabel("Profit")
        st.pyplot(fig)

    # Recommendations and Insights
    st.header("Recommendations and Insights")
    st.subheader("Key Findings:")
    st.write("""
    - Focus on the top-performing products to maximize revenue.
    - Evaluate the impact of discounts on profits for different segments.
    - Identify underperforming products and assess the reasons behind their performance.
    """)
else:
    st.info("Please upload a CSV file to proceed.")
