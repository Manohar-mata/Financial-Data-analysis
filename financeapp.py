import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Title of the Streamlit App
st.title("Airline Sentiment Analysis")

# Load the dataset
@st.cache
def load_data():
    url = "Tweets.csv"
    return pd.read_csv(url)

df = load_data()

# Sidebar for data exploration
st.sidebar.header("Data Exploration")
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw Dataset")
    st.write(df)

# Display dataset information
st.subheader("Dataset Overview")
st.write(f"**Shape of the dataset:** {df.shape}")
st.write(f"**First few rows:**")
st.write(df.head())

# Sentiment Distribution
st.subheader("Sentiment Distribution")

# Barplot of sentiment counts
st.write("**Barplot of Sentiment Counts:**")
sentiment_counts = df['airline_sentiment'].value_counts()
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="coolwarm", ax=ax1)
ax1.set_title("Sentiment Counts")
ax1.set_xlabel("Sentiment")
ax1.set_ylabel("Number of Tweets")
st.pyplot(fig1)

# Pie chart of sentiment distribution
st.write("**Pie Chart of Sentiment Distribution:**")
fig2, ax2 = plt.subplots(figsize=(8, 8))
sentiment_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=["#ff9999","#66b3ff","#99ff99"], ax=ax2)
ax2.set_title("Airline Sentiment Distribution")
ax2.set_ylabel('')
st.pyplot(fig2)

# Tweet Count by Airline and Sentiment
st.subheader("Tweet Count by Airline and Sentiment")
st.write("**Barplot of Tweets by Airline and Sentiment:**")
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.countplot(x='airline', data=df, hue='airline_sentiment', palette='Set2', ax=ax3)
ax3.set_title('Tweet Count by Airline and Sentiment')
ax3.set_xlabel('Airline')
ax3.set_ylabel('Number of Tweets')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
ax3.legend(title='Sentiment')
st.pyplot(fig3)
