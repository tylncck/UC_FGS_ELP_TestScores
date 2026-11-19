# ELP Test and Cumulative GPA Statistical Analysis

- **Author:** Taylan Cicek
- **Institution:** University of Calgary - Faculty of Graduate Studies
- **Contact:** onurtaylan.cicek@ucalgary.ca

This project analyzes the relationship between English Language Proficiency (ELP) test submissions and graduate student outcomes at the University of Calgary. It compares cumulative GPA and discontinuation rates across the most common ELP test categories and produces an exploratory Jupyter notebook report.

The main findings are observational. They do not establish that taking or requiring a particular ELP test causes a GPA or continuation outcome.

## Contents

- [Overview](#overview)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [SQL Server access](#sql-server-access)
- [Running the analysis](#running-the-analysis)
- [Methods](#methods)
- [Reports](#reports)
- [Limitations](#limitations)

## Overview

The notebook pulls graduate student enrollment and ELP test data from SQL Server, identifies the most recent ELP test recorded for each student, and groups students as IELTS, TOEFL, Duolingo, or "No Test" for the main comparison.

The analysis evaluates:

- Differences in cumulative GPA across ELP test groups.
- Differences in student discontinuation rates across ELP test groups.
- Normality and homogeneity assumptions for parametric statistical tests.
- Parametric and non-parametric GPA comparisons.
- Pairwise discontinuation comparisons using Fisher's exact test.

## Project structure

```text
ELP_GPA_StatisticalTests.ipynb  Main analysis notebook
requirements.txt                 Python dependencies
scripts/
  functions.py                   Data-pull and statistical helper functions
  __init__.py                    Python package marker
sql_queries/
  AllTests.sql                   Extracts and categorizes recorded ELP tests
  Query.sql                      Builds the analysis dataset
reports/
  *.html                         Exported notebook report
  *.pdf                          Exported PDF reports
.venv/                          Project virtual environment
```

## Requirements

- Windows
- Python 3.14.3 (the existing `.venv` was created with Python 3.14.3)
- Microsoft ODBC Driver 17 for SQL Server
- An active network connection and access to the University of Calgary data warehouse
- Admin VPN connection

Python packages are listed in [requirements.txt](requirements.txt). The project uses pandas, SQLAlchemy, pyodbc, SciPy, Matplotlib, Plotly, Seaborn, pymssql, and Jupyter.

## Setup

From the project root, activate the existing virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

If you need to create a new environment, use a compatible Python installation:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install Microsoft ODBC Driver 17 for SQL Server if it is not already available. The data-pull helper uses the Windows trusted connection and ODBC Driver 17:

```text
SERVER=ITAPPROREPP01
DATABASE=UofC_DW_Student
DRIVER=ODBC Driver 17 for SQL Server
```

## SQL Server access

**You must be connected to the organization Admin VPN to pull data from the SQL Server.**

After connecting to the Admin VPN, run the notebook while signed into Windows with permissions to access `ITAPPROREPP01` and `UofC_DW_Student`. The project uses `Trusted_Connection=yes`; database credentials are not stored in the notebook or source files.

Without the Admin VPN connection or the required SQL Server permissions, `data_pull()` will fail to connect.

## Running the analysis

1. Connect to the Admin VPN.
2. Open a PowerShell window in the project root.
3. Activate the virtual environment:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Start Jupyter:

   ```powershell
   jupyter notebook
   ```

5. Open `ELP_GPA_StatisticalTests.ipynb`.
6. Run all cells from the beginning.

The notebook loads [sql_queries/AllTests.sql](sql_queries/AllTests.sql) and [sql_queries/Query.sql](sql_queries/Query.sql) through `scripts/functions.py`.

To run the notebook non-interactively:

```powershell
jupyter execute ELP_GPA_StatisticalTests.ipynb
```

## Methods

### Data preparation

The SQL queries:

- Identify English proficiency test components recorded in `F_External_Tests`.
- Keep the best recorded ELP result dated from 2020-01-01 onward.
- Map test component codes to test names.
- Select the latest ELP test for each student.
- Identify cancellations or withdrawals for eligible international graduate students.
- Join enrollment, cumulative GPA, discontinuation, and ELP test data.

The Python helpers remove GPA outliers using an interquartile range rule, calculate descriptive summaries, and generate visualizations.

### Statistical analysis

The notebook uses:

- Shapiro-Wilk tests for within-group normality.
- Box-Cox transformation as a normality diagnostic.
- Bartlett's test for homogeneity of variance.
- ANOVA and Bonferroni-corrected pairwise t-tests as exploratory parametric checks.
- Kruskal-Wallis and pairwise Mann-Whitney U tests as non-parametric alternatives.
- Fisher's exact test for pairwise discontinuation rate comparisons.

The main GPA analysis retains TOEFL, IELTS, Duolingo, and "No Test" and removes GPA outliers using the 1.5 x IQR rule.

## Reports

Generated HTML and PDF outputs are stored in [reports/](reports/).

## Limitations

- The analysis is exploratory and observational.
- It does not control for academic program, country of origin, admission timing, prior study, or other potentially confounding variables.
- Some ELP test categories have substantially more records than others.
- Outlier removal and test-category filtering change the population represented in the statistical models.
- Group distributions were non-normal, so interpret parametric ANOVA and t-test outputs cautiously.
- Mann-Whitney U tests are unadjusted for multiple comparisons.
- Fisher's exact pairwise tests are unadjusted and do not replace an omnibus analysis.
