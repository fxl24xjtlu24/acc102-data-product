# acc102-data-product
# ESG & Financial Performance Dashboard

## 1. Problem & User
This project investigates whether a company's ESG (Environmental, Social, Governance) score correlates with financial metrics (profit margin, revenue, market cap, growth rate). Target users are investors and corporate sustainability analysts who want to assess ESG as a non-financial risk factor.

## 2. Data
- **Source**: Kaggle – "Synthetic ESG & Financial Performance Dataset" by Shreyash Jagtap (1 CSV file, 388 kB, 7,523 downloads)
- **Access date**: April 2026
- **Key fields**: `ESG_Overall`, `ESG_Social`, `ESG_Governance`, `ProfitMargin`, `Revenue`, `MarketCap`, `GrowthRate`, `Industry`, `ESG_Category` (derived)

## 3. Methods
- Data cleaning with pandas (drop missing values, create ESG categories via quantiles)
- Visualizations: scatter plot (ESG vs. profit margin by industry), bar chart (average profit margin by ESG category), correlation heatmap (ESG dimensions + financial metrics)
- Interactive dashboard built with Streamlit

## 4. Key Findings
- ESG overall score has a very weak positive correlation with profit margin (~0.09)
- High-ESG companies show only slightly higher average profit margin than low-ESG ones (difference <2%)
- Revenue and market cap are strongly correlated (0.84)
- Industry differences matter: e.g., Finance & Technology have high ESG scores but not necessarily the highest margins

## 5. How to run
pip install -r requirements.txt
streamlit run app.py

## 6. Product link / Demo
Product link   https://github.com/fxl24xjtlu24/acc102-data-product.git

 
## 7. Limitations & next steps

· Cross-sectional data → cannot infer causality
· Missing control variables (firm size, leverage, R&D spending)
· ESG scores from a single provider; results may not generalize
· Next steps: panel data analysis, regression with industry fixed effects, statistical significance tests (t-test/ANOVA)
