---
description: Automated Exploratory Data Analysis (EDA) of local or uploaded datasets.
---

# EDA Workflow

This workflow guides the agent through a standard EDA process to understand data structure, distributions, and initial correlations.

## Steps

1. **Information Gathering**
   - Check file format (CSV, Parquet, Excel).
   - Get basic stats: `df.describe()`, `df.info()`.
   - Identify missing values and data types.

2. **Statistical Analysis**
   - Calculate skewness and kurtosis for numerical columns.
   - Perform Shapiro-Wilk test for normality on key variables.
   - Generate correlation matrix (Pearson/Spearman).

3. **Data Visualization**
   - Save histograms for all numerical features to `plots/eda/histograms/`.
   - Save boxplots for outlier detection to `plots/eda/outliers/`.
   - Save a heatmap of the correlation matrix to `plots/eda/correlations/`.

4. **Planning & Recommendations**
   - Document findings in `EDA_SUMMARY.md`.
   - Suggest potential ML features or data cleaning steps.
