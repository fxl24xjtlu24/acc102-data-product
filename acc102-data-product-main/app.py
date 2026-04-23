import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Page configuration ----------
st.set_page_config(page_title="ESG & Financial Dashboard", layout="wide")
st.title("🌿 ESG & Financial Performance Dashboard")
st.markdown("Explore the relationship between ESG scores and financial metrics across companies, industries, and time.")

# ---------- Data loading with caching ----------
@st.cache_data
def load_data():
    df = pd.read_csv("esg_data.csv")
    # Create ESG category based on tertiles of ESG_Overall
    df["ESG_Category"] = pd.qcut(df["ESG_Overall"], q=3, labels=["Low", "Medium", "High"])
    return df

df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("🔍 Filters")

# Industry multi-select
industries = st.sidebar.multiselect(
    "Industry",
    options=sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

# Year range slider
years = sorted(df["Year"].unique())
year_range = st.sidebar.slider(
    "Year Range",
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years))
)

# Company multi-select (optional)
companies = st.sidebar.multiselect(
    "Company (optional, leave empty for all)",
    options=sorted(df["CompanyName"].unique()),
    default=[]
)

# ---------- Apply filters ----------
filtered = df[
    (df["Industry"].isin(industries)) &
    (df["Year"].between(year_range[0], year_range[1]))
]
if companies:
    filtered = filtered[filtered["CompanyName"].isin(companies)]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your filters.")
    st.stop()

st.markdown(f"**Showing data for {len(filtered['CompanyName'].unique())} companies | {len(filtered)} records**")

# Define column groups for reuse
esg_cols = ["ESG_Overall", "ESG_Environmental", "ESG_Social", "ESG_Governance"]
financial_cols = ["ProfitMargin", "Revenue", "MarketCap", "GrowthRate"]

# ==================== Visualization 1 ====================
st.subheader("1. ESG Overall Score vs Profit Margin")
fig1, ax1 = plt.subplots(figsize=(10, 6))

sns.scatterplot(
    data=filtered, x="ESG_Overall", y="ProfitMargin",
    hue="Industry", style="ESG_Category", alpha=0.7, ax=ax1
)

# Add linear trend line with slope annotation
z = np.polyfit(filtered["ESG_Overall"], filtered["ProfitMargin"], 1)
p = np.poly1d(z)
ax1.plot(filtered["ESG_Overall"].sort_values(), p(filtered["ESG_Overall"].sort_values()),
         "k--", linewidth=1, label=f"Trend (slope={z[0]:.3f})")
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.set_xlabel("ESG Overall Score")
ax1.set_ylabel("Profit Margin (%)")
st.pyplot(fig1)

# ==================== Visualization 2 ====================
st.subheader("2. Average Profit Margin by ESG Category (with Std Dev Error Bars)")
avg_profit = filtered.groupby("ESG_Category")["ProfitMargin"].mean().reset_index()
std_profit = filtered.groupby("ESG_Category")["ProfitMargin"].std().reset_index()
avg_profit["std"] = std_profit["ProfitMargin"]

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_profit, x="ESG_Category", y="ProfitMargin", palette="viridis", ax=ax2)
ax2.errorbar(x=range(len(avg_profit)), y=avg_profit["ProfitMargin"], yerr=avg_profit["std"],
             fmt='none', c='black', capsize=5)
for i, row in avg_profit.iterrows():
    ax2.text(i, row["ProfitMargin"] + 0.5, f"{row['ProfitMargin']:.1f}%", ha='center')
ax2.set_ylabel("Average Profit Margin (%)")
st.pyplot(fig2)

# ==================== Visualization 3 ====================
st.subheader("3. Profit Margin Trend Over Time by ESG Category")
trend_data = filtered.groupby(["Year", "ESG_Category"])["ProfitMargin"].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=trend_data, x="Year", y="ProfitMargin", hue="ESG_Category", marker="o", ax=ax3)
ax3.set_ylabel("Average Profit Margin (%)")
ax3.set_title("Profit Margin Trend by ESG Category")
st.pyplot(fig3)

# ==================== Visualization 3b ====================
st.subheader("3b. ESG Overall Score Trend by Industry")
trend_esg = filtered.groupby(["Year", "Industry"])["ESG_Overall"].mean().reset_index()
fig3b, ax3b = plt.subplots(figsize=(12, 5))
sns.lineplot(data=trend_esg, x="Year", y="ESG_Overall", hue="Industry", marker="o", ax=ax3b)
ax3b.set_ylabel("Average ESG Overall Score")
ax3b.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig3b)

# ==================== Visualization 4 ====================
st.subheader("4. Correlation Matrix: ESG Dimensions vs Financial Metrics")
corr_cols = esg_cols + financial_cols
corr_data = filtered[corr_cols].dropna()
corr_matrix = corr_data.corr()

fig4, ax4 = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap="coolwarm", center=0,
            fmt=".2f", linewidths=0.5, ax=ax4)
ax4.set_title("Correlation Matrix (Upper Triangle)")
st.pyplot(fig4)

# ==================== Visualization 5 ====================
st.subheader("5. Industry Bubble Chart: ESG Score vs Profit Margin (Size = Market Cap)")
industry_agg = filtered.groupby("Industry").agg({
    "ESG_Overall": "mean",
    "ProfitMargin": "mean",
    "MarketCap": "mean"
}).reset_index()

fig5, ax5 = plt.subplots(figsize=(10, 6))
scatter = ax5.scatter(
    industry_agg["ESG_Overall"], industry_agg["ProfitMargin"],
    s=industry_agg["MarketCap"] / 1e6,   # Scale marker size to millions
    alpha=0.6, c=range(len(industry_agg)), cmap="tab10"
)
for i, row in industry_agg.iterrows():
    ax5.annotate(row["Industry"], (row["ESG_Overall"], row["ProfitMargin"]), fontsize=9)
ax5.set_xlabel("Average ESG Overall Score")
ax5.set_ylabel("Average Profit Margin (%)")
ax5.set_title("Bubble size = Average Market Cap (million USD)")
st.pyplot(fig5)

# ==================== Visualization 6 ====================
st.subheader("6. Revenue vs Market Cap (Log-Log Scale with Correlation)")
fig6, ax6 = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=filtered, x="Revenue", y="MarketCap", hue="Industry", alpha=0.6, ax=ax6)
ax6.set_xscale("log")
ax6.set_yscale("log")
ax6.set_xlabel("Revenue (log scale)")
ax6.set_ylabel("Market Cap (log scale)")
corr_val = filtered[["Revenue", "MarketCap"]].corr().iloc[0,1]
ax6.set_title(f"Revenue vs Market Cap (log-log) | Correlation: {corr_val:.2f}")
st.pyplot(fig6)

# ==================== Summary Statistics ====================
st.subheader("📊 Summary Statistics (Filtered Data)")
st.dataframe(filtered[esg_cols + financial_cols].describe())

# ==================== Data Source ====================
st.markdown("---")
st.caption("Data Source: Kaggle - Synthetic ESG & Financial Performance Dataset by Shreyash Jagtap")
