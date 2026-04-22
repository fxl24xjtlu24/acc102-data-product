import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Data Cleaning ----------
def clean_data(df):
    # Drop empty columns
    df = df.dropna(axis=1, how='all')
    # Drop any columns containing 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains('Unnamed')]
    
    # Convert numeric columns
    numeric_cols = ['Revenue', 'ProfitMargin', 'MarketCap', 'GrowthRate',
                    'ESG_Overall', 'ESG_Environment', 'ESG_Social', 'ESG_Governance',
                    'CarbonEmissions', 'WaterUsage', 'EnergyConsumption']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows missing key metrics
    df = df.dropna(subset=['ProfitMargin', 'ESG_Overall'])
    
    # Create ESG category
    df['ESG_Category'] = pd.cut(df['ESG_Overall'],
                                bins=[0, 40, 60, 100],
                                labels=['Low', 'Medium', 'High'])
    # Profitability flag
    df['Profitable'] = df['ProfitMargin'] > 0
    # Ensure Year is integer
    df['Year'] = df['Year'].astype(int)
    return df

# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_csv('esg_data.csv')
    df = clean_data(df)
    return df

df = load_data()

# ---------- Page Config ----------
st.set_page_config(page_title="ESG & Financial Dashboard", layout="wide")
st.title("🌿 ESG and Financial Performance Explorer")
st.markdown("Explore the relationship between ESG scores and financial metrics.")

# ---------- Sidebar Filters ----------
st.sidebar.header("Filter Data")
industry = st.sidebar.selectbox("Industry", ['All'] + sorted(df['Industry'].dropna().unique()))
region = st.sidebar.selectbox("Region", ['All'] + sorted(df['Region'].dropna().unique()))
year_range = st.sidebar.slider("Year Range", int(df['Year'].min()), int(df['Year'].max()), (2015, 2025))
esg_cat = st.sidebar.selectbox("ESG Category", ['All', 'Low', 'Medium', 'High'])

# Apply filters
filtered = df.copy()
if industry != 'All':
    filtered = filtered[filtered['Industry'] == industry]
if region != 'All':
    filtered = filtered[filtered['Region'] == region]
filtered = filtered[(filtered['Year'] >= year_range[0]) & (filtered['Year'] <= year_range[1])]
if esg_cat != 'All':
    filtered = filtered[filtered['ESG_Category'] == esg_cat]

st.sidebar.metric("Records after filter", len(filtered))

# ---------- Visualizations ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 ESG Overall vs Profit Margin")
    if not filtered.empty:
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered, x='ESG_Overall', y='ProfitMargin', hue='Industry', alpha=0.7, ax=ax)
        ax.axhline(0, color='red', linestyle='--')
        ax.set_xlabel("ESG Overall Score")
        ax.set_ylabel("Profit Margin (%)")
        st.pyplot(fig)
    else:
        st.info("No data for selected filters.")

with col2:
    st.subheader("📈 Avg Profit Margin by ESG Category")
    if not filtered.empty:
        avg = filtered.groupby('ESG_Category')['ProfitMargin'].mean().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(data=avg, x='ESG_Category', y='ProfitMargin', palette='viridis', ax=ax)
        ax.set_ylabel("Avg Profit Margin (%)")
        st.pyplot(fig)
    else:
        st.info("No data.")

# Correlation heatmap
st.subheader("📉 Correlation Matrix (ESG vs Financial Metrics)")
if len(filtered) > 5:
    corr_cols = ['ESG_Overall', 'ESG_Environment', 'ESG_Social', 'ESG_Governance',
                 'ProfitMargin', 'Revenue', 'MarketCap', 'GrowthRate']
    existing = [c for c in corr_cols if c in filtered.columns]
    if len(existing) >= 2:
        corr = filtered[existing].corr()
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
        st.pyplot(fig)

# Data table
st.subheader("📋 Filtered Data (first 100 rows)")
st.dataframe(filtered.head(100))

# Key insights
st.markdown("---")
st.subheader("💡 Key Insights")
if not filtered.empty:
    corr_val = filtered['ESG_Overall'].corr(filtered['ProfitMargin'])
    st.write(f"- Correlation between ESG Overall and Profit Margin: **{corr_val:.2f}**")
    high = filtered[filtered['ESG_Category']=='High']['ProfitMargin'].mean()
    low = filtered[filtered['ESG_Category']=='Low']['ProfitMargin'].mean()
    if pd.notna(high) and pd.notna(low):
        diff = high - low
        st.write(f"- High ESG companies have **{diff:.2f}%** higher profit margin than Low ESG companies.")
st.caption("Data source: Kaggle ESG and Financial Performance Dataset (April 2026)")