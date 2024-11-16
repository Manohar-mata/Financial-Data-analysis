import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit app title
st.title("Sales and Profit Analysis")

# Load your data
# Assuming `df_dummy` is already available or being loaded from a source
# Example: df_dummy = pd.read_csv('your_data.csv')
df_dummy = pd.DataFrame({  # Dummy data for example purposes
    'product': ['A', 'A', 'B', 'B', 'C', 'C'],
    'month_name': ['January', 'February', 'January', 'February', 'January', 'February'],
    'sales($)': [5000000, 6000000, 7000000, 8000000, 2000000, 3000000],
    'profit($)': [1000000, 1200000, 1400000, 1600000, 400000, 600000]
})

# Group data by product and month_name, then sum sales
sales_by_product_month = df_dummy.groupby(['product', 'month_name'])['sales($)'].sum().unstack()

# Bar chart: Sales by Product and Month
st.subheader("Sales by Product and Month")
fig1, ax1 = plt.subplots(figsize=(15, 8))
sales_by_product_month.plot(kind='bar', ax=ax1)
ax1.set_title('Sales by Product and Month')
ax1.set_xlabel('Product')
ax1.set_ylabel('Total Sales')
ax1.set_xticklabels(ax1.get_xticks(), rotation=45, ha='right')
ax1.legend(title='Month')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
st.pyplot(fig1)

# Group data by month_name and calculate the sum of profit for each month
profit_by_month = df_dummy.groupby('month_name')['profit($)'].sum().sort_values(ascending=True)

# Line chart: Trend in Profitability Across Months
st.subheader("Trend in Profitability Across Months")
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(profit_by_month.index, profit_by_month.values, marker='o')
ax2.set_title('Trend in Profitability Across Months')
ax2.set_xlabel('Month')
ax2.set_ylabel('Total Profit ($)')
ax2.tick_params(axis='x', rotation=45)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
ax2.grid(True)
st.pyplot(fig2)
