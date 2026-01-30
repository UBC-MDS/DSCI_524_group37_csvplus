# csvplus

|        |        |
|--------|--------|
| CI/CD  | [![CI](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/actions/workflows/build.yml) [![codecov](https://codecov.io/github/UBC-MDS/DSCI_524_group37_csvplus/graph/badge.svg?token=zmpNtn6nI6)](https://codecov.io/github/UBC-MDS/DSCI_524_group37_csvplus) |
| Package | [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) |
| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |



> **Note**: PyPI badges are included for completeness but may not reflect a published package.

---

## Overview

`csvplus` is a lightweight Python package that provides **practical utilities for loading, comparing, cleaning, and summarizing tabular data**.  
While some functions operate directly on CSV files, others are designed to work with **pandas DataFrames**, making the package flexible for different stages of a data analysis workflow.

The package is intended to support:

- Memory-efficient data loading
- Dataset version comparison and auditing
- Data cleaning and standardization
- Exploratory data analysis and data quality checks

---

## Core Functions

This package addresses common data preprocessing and exploration tasks through the following functions:

|Function    |Description    |
|--------|--------|
|`load_optimized_csv`|Loads a CSV file and automatically downcasts data types to minimize memory footprint.|
|`data_version_diff`|Compare two versions of a pandas DataFrame and return a structured summary of schema, row count, missing values, numeric statistics, and data type changes.|
|`resolve_string_value`|Consolidating spelling variations of the same data value in a column.|
|`summary_report`|Produce a list of descriptive statistics of the data and information about missing values.|

Some functions operate on **CSV files**, while others work directly on **pandas DataFrames**, allowing users to integrate `csvplus` into existing pandas-based workflows.

Our package fits into the Python preprocessing framework. Currently, the [`pandas`](https://pandas.pydata.org/) package provides basic functionality to read CSV and produce summary statistics, and the [`pyjanitor`](https://pyjanitor-devs.github.io/pyjanitor/) package provides functions for sanitizing the column names and converting column dtype.

`csvplus` extends these tools with automated memory optimization, dataset version comparison and high-level summaries useful for auditing and exploratory analysis

Full API reference and examples are available at: https://ubc-mds.github.io/DSCI_524_group37_csvplus/reference/
---

## Get started

### Installation (from Test Pypi)

Install the latest test version from test PyPI

```bash
# 1. Create and activate a new Python 3.11 environment (recommended)
conda create -n py311 python=3.11 -y
conda activate py311

# 2. Upgrade pip to ensure latest package handling
pip install --upgrade pip

# 3. (macOS users only) Install rapidfuzz first to avoid build issues
pip install rapidfuzz

# 4. Install csvplus from Test PyPI
pip install --index-url https://test.pypi.org/simple/  --extra-index-url https://pypi.org/simple csvplus

```

> Note: Step 3 is only required on macOS due to a known rapidfuzz build issue. On Linux or Windows, pip will install dependencies automatically.

Or install from PyPI (once published)

```bash
pip install csvplus
```

## Usage Examples

```python
import pandas as pd
from csvplus.data_version_diff import data_version_diff, display_data_version_diff
from csvplus.load_optimized_csv import load_optimized_csv
from csvplus.data_correction import resolve_string_value
from csvplus.generate_report import summary_report

# --- compare two DataFrame versions ---
df_old = pd.DataFrame({"id": [1,2,3], "value": [10,20,30]})
df_new = pd.DataFrame({"id": [1,2,3,4], "value": [10,25,30,40], "category": ["A","B",None,"C"], "amount": [100,200,300,400]})

diff = data_version_diff(df_old, df_new)
display_data_version_diff(diff)

# --- resolve string value --
df1 = pd.DataFrame({ "company": ["Google", "Gooogle", "Gogle", "Microsoft", "Microsof"]})
resolve_string_value(df1, column="company", canonical_values=["Google", "Microsoft"],threshold=80)
print(df)

# --- load a CSV file with optimized memory usage ---
df = load_optimized_csv("large_dataset.csv")
print(df1.dtypes) 

# --- Generate summary statistics ---
numeric_stats, categorical_stats = summary_report(df)
print(numeric_stats.head())
print(categorical_stats.head())
```

## Developers

### Development Setup

Create conda environment and clone the repo.

```bash
conda env create -f environment.yml
conda activate csvplus

git clone https://github.com/UBC-MDS/DSCI_524_group37_csvplus
cd DSCI_524_group37_csvplus
```

### Run Tests and Coverage

All tests are written using `pytest`. To run the full test suite and generate a coverage report execute:

```bash
# install coverage tools if not yet installed
pip install pytest pytest-cov

pytest --cov=csvplus --cov-report=term-missing
```

### Install csvplus package (editable mode)

This allows you to edit the source code locally while using the package.

```bash
pip install -e .
```

### Build and Preview Documentation

```bash
quartodoc build
quarto preview 
quarto render
```

## Contributors

- Alan Liu
- Oswin Gan
- Purity Jangaya
- Ralah Aaqil

## License

- Copyright © 2026
- Free software distributed under the [MIT License](./LICENSE).
