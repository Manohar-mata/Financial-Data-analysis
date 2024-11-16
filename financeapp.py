
import streamlit as st
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Sales Data Analysis Dashboard")

# Upload data file
uploaded_file = st.file_uploader("Financials.csv", type="csv")

if uploaded_file is not None:
    df_dummy = pd.read_csv(uploaded_file)

    # Perform data cleaning and preprocessing
    df_dummy.iloc[:, 4:12] = df_dummy.iloc[:, 4:12].apply(
        lambda x: x.str.replace(',', '')
                 .str.replace('(', '-')
                 .str.replace(')', '')
                 .str.strip()
                 .replace('-', np.nan)
                 .replace('', np.nan)
    )

    df_dummy['profit($)'] = df_dummy['profit($)'].astype(float)
    df_dummy['profit($)'] = df_dummy['profit($)'].fillna(df_dummy['profit($)'].mean())

    df_dummy['manufacturing_price($)'] = df_dummy['manufacturing_price($)'].astype(float)
    df_dummy['sale_price($)'] = df_dummy['sale_price($)'].astype(float)
    df_dummy['gross_sales($)'] = df_dummy['gross_sales($)'].astype(float)
    df_dummy['discounts($)'] = df_dummy['discounts($)'].astype(float)
    df_dummy['sales($)'] = df_dummy['sales($)'].astype(float)
    df_dummy['cogs($)'] = df_dummy['cogs($)'].astype(float)
    df_dummy['profit($)'] = df_dummy['profit($)'].astype(float)
    df_dummy['units_sold($)'] = df_dummy['units_sold($)'].astype(float)
    df_dummy['date'] = pd.to_datetime(df_dummy['date'], errors='coerce')

    # Descriptive statistics
    st.subheader("Descriptive Statistics")
    st.write(df_dummy.describe())

    # Visualizations
    st.subheader("Overall Performance and Trends")

    # Sales by Product and Month
    sales_by_product_month = df_dummy.groupby(['product', 'month_name'])['sales($)'].sum().unstack()
    st.bar_chart(sales_by_product_month)

    # Trend in Profitability Across Months
    profit_by_month = df_dummy.groupby('month_name')['profit($)'].sum()
    st.line_chart(profit_by_month)

    # Revenue Contribution by Product
    product_revenue = df_dummy.groupby('product')['sales($)'].sum().sort_values(ascending=False)
    st.bar_chart(product_revenue)

    # Trend in Unit Sales Across Months
    units_sold_by_month = df_dummy.groupby('month_name')['units_sold($)'].sum()
    st.line_chart(units_sold_by_month)

    st.subheader("Product-Specific Insights")

    # Product Performance: Sales and Profit
    product_performance = df_dummy.groupby('product').agg({'sales($)': 'sum', 'profit($)': 'sum'})
    product_performance = product_performance.sort_values('sales($)', ascending=False)
    st.bar_chart(product_performance[['sales($)', 'profit($)']])

    st.subheader("Segmentation Analysis")

    # Sales Trend Across Months by Segment
    for segment in df_dummy['segment'].unique():
        sales_segment_month = df_dummy[df_dummy['segment'] == segment].groupby('month_name')['sales($)'].sum()
        st.line_chart(sales_segment_month)

    # Revenue Contribution by Segment
    segment_revenue = df_dummy.groupby('segment')['sales($)'].sum().sort_values(ascending=False)
    st.bar_chart(segment_revenue)

    # Profit Margin Comparison Across Segments
    segment_profit_margin = df_dummy.groupby('segment').apply(
        lambda x: (x['profit($)'].sum() / x['sales($)'].sum()) * 100 if x['sales($)'].sum() > 0 else 0)
    st.bar_chart(segment_profit_margin)

    st.subheader("Discount Impact Analysis")

    # Impact of Discount Bands on Sales and Profitability
    discount_impact = df_dummy.groupby('discount_band').agg({'sales($)': 'sum', 'profit($)': 'sum'})
    st.bar_chart(discount_impact[['sales($)', 'profit($)']])

    # Discount Effectiveness by Product and Month
    discount_effectiveness = df_dummy.groupby(['discount_band', 'product', 'month_name'])['sales($)'].sum().reset_index()
    discount_effectiveness_pivot = discount_effectiveness.pivot_table(index=['discount_band', 'product'],
                                                                     columns='month_name', values='sales($)').fillna(0)
    st.write("Discount Effectiveness Heatmap:")
    st.pyplot(sns.heatmap(discount_effectiveness_pivot, annot=True, fmt=".0f", cmap='viridis'))

    st.subheader("Country-Wise Comparison")

    # Sales Performance Comparison Across Countries
    country_sales = df_dummy.groupby('country')['sales($)'].sum().sort_values(ascending=False)
    st.bar_chart(country_sales)

    # Profitability Comparison Across Countries
    country_profit = df_dummy.groupby('country')['profit($)'].sum().sort_values(ascending=False)
    st.bar_chart(country_profit)

    # Seasonal Variation in Sales
    st.subheader("Seasonal Variation in Sales")
    st.line_chart(df_dummy.groupby('month_name')['sales($)'].sum())

    # Download cleaned data
    st.download_button(label="Download Cleaned Data",
                       data=df_dummy.to_csv(index=False).encode('utf-8'),
                       file_name='cleaned_sales_data.csv',
                       mime='text/csv')

else:
    st.info("Please upload a CSV file to begin analysis.")
