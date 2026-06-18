# Degree and Employment Analysis

## Project overview

This project analyzes employment outcomes of recent tertiary graduates in Greece compared with the European Union, using Eurostat data.

The project uses Python for data collection, cleaning, exploratory analysis and visualization, and R for statistical modelling.

## Research question

To what extent is tertiary education associated with employment outcomes among recent graduates, and how does Greece compare with the European Union over time?

## Data source

Data source: Eurostat dataset `edat_lfse_24`.

Main filters:

- Age group: 20–34
- Duration since graduation: 1–3 years
- Education level: ISCED 5–8, tertiary education
- Unit: percentage
- Geography: Greece, EU27_2020 and European countries
- Period: 2014–2025

## Tools used

- Python
  - pandas
  - requests
  - matplotlib
  - Jupyter Notebook

- R
  - tidyverse
  - broom
  - ggplot2
  - linear regression

## Repository structure

```text
degree-employment-analysis/
├── data/
│   └── processed/
├── notebooks/
│   └── 01_eda.ipynb
├── src/
│   └── download_eurostat.py
├── R/
│   └── 01_statistical_analysis.R
├── outputs/
│   ├── figures/
│   └── tables/
├── requirements.txt
└── README.md

Methodology

The project follows these steps:

1. Download Eurostat data through the API.
2. Convert JSON-stat data into a tidy tabular format.
3. Filter the dataset for recent tertiary graduates.
4. Compare Greece with the European Union over time.
5. Rank European countries by the latest available employment rate.
6. Estimate a linear trend model in R.

Key findings

The analysis shows that Greece has historically had lower employment rates for recent tertiary graduates compared with the European Union average.

The R trend model suggests that Greece improved faster over time, meaning the gap with the EU narrowed during the period examined.

Outputs

Main figures:

* outputs/figures/greece_vs_eu_tertiary_graduates.png
* outputs/figures/country_ranking.png
* outputs/figures/r_employment_trend.png

Main tables:

* outputs/tables/greece_vs_eu_comparison.csv
* outputs/tables/country_ranking.csv
* outputs/tables/r_summary_statistics.csv
* outputs/tables/r_regression_results.csv

Limitations

This project identifies associations and trends, not causal effects. It does not prove that obtaining a degree directly causes employment.

Other factors such as macroeconomic conditions, labour market structure, migration, field of study and work experience may also affect employment outcomes.

Conclusion

This project demonstrates how public labour market data can be used to analyze education-to-employment transitions. It is suitable for a data analytics portfolio because it includes data collection, cleaning, visualization, statistical modelling and reproducible code.
