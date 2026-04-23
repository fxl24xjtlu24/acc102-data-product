# ESG & Financial Performance Dashboard

## 1. Problem & User
This project investigates whether a company's ESG (Environmental, Social, Governance) score correlates with key financial metrics: profit margin, revenue, market cap, and growth rate. Target users are investors and corporate sustainability analysts who want to assess ESG as a non-financial risk factor.

## 2. Data
- **Source**: Kaggle – "Synthetic ESG & Financial Performance Dataset" by Shreyash Jagtap (1 CSV file, 388 kB, 7,523 downloads)
- **Access date**: April 2026
- **Key fields**: `ESG_Overall`, `ESG_Environmental`, `ESG_Social`, `ESG_Governance`, `ProfitMargin`, `Revenue`, `MarketCap`, `GrowthRate`, `Industry`, `Year`, `CompanyName`

## 3. Methods
- Data cleaning with pandas (drop missing values, create ESG categories via tertiles)
- Visualizations:
  - Scatter plot (ESG overall vs. profit margin) with trend line
  - Bar chart (average profit margin by ESG category) with standard deviation error bars
  - Line plots: profit margin trend over time by ESG category; ESG overall trend by industry
  - Correlation heatmap (ESG dimensions + financial metrics)
  - Industry bubble chart (ESG score vs. profit margin, bubble size = market cap)
  - Log-log scatter plot (revenue vs. market cap) with correlation annotation
- Interactive dashboard built with Streamlit; static analysis notebook in Jupyter

## 4. Key Findings
- ESG overall score has a very weak positive correlation with profit margin (~0.09)
- High-ESG companies show only slightly higher average profit margin than low-ESG ones (difference <2.5%) – bar chart with error bars confirms overlap
- Revenue and market cap are strongly correlated (0.84)
- Industry differences matter: e.g., Finance & Technology have high ESG scores but not necessarily the highest margins
- Time trends show profit margins for all ESG categories remained relatively stable, with High ESG performing marginally better in recent years

## 5. How to run
pip install -r requirements.txt

streamlit run app.py

## 6. Product link / Demo

· GitHub repository: https://github.com/fxl24xjtlu24/acc102-data-product.git

· Demo video: 

## 7. Limitations & next steps

· Cross-sectional data cannot infer causality
· Missing control variables (firm size, leverage, R&D spending)
· ESG scores from a single provider; results may not generalize

· Next steps: panel data analysis, regression with industry fixed effects, statistical significance tests (t-test/ANOVA)
