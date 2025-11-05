# W.MSCIDS_CIP02.H25_BB_MT_XS
Research project for the module "Data colection, Integration and Preprocessing" exploring links between environmental, social, and governance (ESG) scores and corporate financial performance.

## Table of Contents

- [W.MSCIDS\_CIP02.H25\_BB\_MT\_XS](#wmscids_cip02h25_bb_mt_xs)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Data Sources](#data-sources)
  - [Usage](#usage)
    - [1. Data Acquisition](#1-data-acquisition)
    - [2. Run Complete Analysis](#2-run-complete-analysis)
    - [3. Generate Report](#3-generate-report)
  - [Code Contribution](#code-contribution)

## Project Structure

```
.
├── README.md
│
├── Code/                              # Code scripts
│   ├── project_code.ipynb             # Complete data cleansing and analysis notebook
│   ├── data_acquisition.py            # Data collection scripts
│   ├── W.MSCIDS_CIP02.H25_BB_MT_XS.code-workspace        # VS Code workspace configuration
│
├── Company_List/                      # Company selection documentation
│   ├── company_list.xlsx              # Detailed cross-checking process for company list
│   ├── S&P_companies.txt              # S&P 500 company tickers
│   └── swiss_companies.txt            # Swiss (SPI) company tickers
│
├── Data/                              # Data files
│   ├── cleaned_combined_data.csv      # Final cleaned dataset for analysis
│   ├── esg_financial_analysis_sp500.csv   # Raw S&P 500 data
│   └── esg_financial_analysis_spi.csv     # Raw SPI data
│
└── Doc/                               # Documentation and reports
    ├── apa.csl                        # Citation style
    ├── feasibility_study.pdf          # Initial feasibility analysis
    ├── final_document.pdf             # Final report (PDF)
    ├── final_document.qmd             # Final report (Quarto source)
    └── references.bib                 # Bibliography
```

## Data Sources

1. **Yahoo Finance API** (`yfinance`)
   - Financial performance metrics (Stock price, Revenue, Market Cap, etc.)
   - ESG Risk Ratings (powered by Sustainalytics)

2. **Index Constituents**
   - [SPI (Swiss Performance Index)](https://en.wikipedia.org/wiki/Swiss_Performance_Index): 201 Swiss-listed companies
   - [S&P 500](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies): 503 largest U.S. companies

## Usage

### 1. Data Acquisition

```python
# Run data acquisition script
python Data/data_acquisition.py
```

This will:
- Fetch financial data for all companies in the ticker lists
- Calculate risk metrics (stock price, market cap, etc.)
- Retrieve ESG scores from Yahoo Finance
- Save raw data to CSV files

### 2. Run Complete Analysis
1. Open the project workspace in VS Code to access all files, notebooks, and settings:

```bash
code W.MSCIDS_CIP02.H25_BB_MT_XS.code-workspace
```

2. Open and run the notebook project_code.ipynb within the workspace for data loading, analysis, and visualization.

### 3. Generate Report

The final report is written in Quarto:

```bash
quarto render Doc/final_document.qmd
```

## Code Contribution

- Xinmeng Song: Data Acquisition, Data Cleansing
- Marisa Timm: RQ1, RQ2
- Bianca Bernasconi: RQ3, RQ4