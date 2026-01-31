# csvplus

|         |                                                                                                                                                                                                                                                                                                                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI/CD   | [![CI](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/DSCI_524_group37_csvplus/actions/workflows/build.yml) [![codecov](https://codecov.io/github/UBC-MDS/DSCI_524_group37_csvplus/graph/badge.svg?token=zmpNtn6nI6)](https://codecov.io/github/UBC-MDS/DSCI_524_group37_csvplus) |
| Package | [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)                                                                                                                                                                                                                                                  |
| Meta    | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)                                                                                                                                                                                                                                   |

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

| Function               | Description                                                                                                                                                 |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `load_optimized_csv`   | Loads a CSV file and automatically downcasts data types to minimize memory footprint.                                                                       |
| `data_version_diff`    | Compare two versions of a pandas DataFrame and return a structured summary of schema, row count, missing values, numeric statistics, and data type changes. |
| `resolve_string_value` | Consolidating spelling variations of the same data value in a column.                                                                                       |
| `summary_report`       | Produce a list of descriptive statistics of the data and information about missing values.                                                                  |

Some functions operate on **CSV files**, while others work directly on **pandas DataFrames**, allowing users to integrate `csvplus` into existing pandas-based workflows.

Our package fits into the Python preprocessing framework. Currently, the [`pandas`](https://pandas.pydata.org/) package provides basic functionality to read CSV and produce summary statistics, and the [`pyjanitor`](https://pyjanitor-devs.github.io/pyjanitor/) package provides functions for sanitizing the column names and converting column dtype.

`csvplus` extends these tools with automated memory optimization, dataset version comparison and high-level summaries useful for auditing and exploratory analysis

## Full API reference and examples are available at: https://ubc-mds.github.io/DSCI_524_group37_csvplus/reference/

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

## Usage Examples

```python
import pandas as pd
from csvplus.data_version_diff import data_version_diff, display_data_version_diff
from csvplus.load_optimized_csv import load_optimized_csv
from csvplus.data_correction import resolve_string_value
from csvplus.generate_report import summary_report

# --- compare two DataFrame versions ---
# Original dataset
df_v1 = pd.DataFrame({
    "id": [1, 2, 3],
    "value": [10, 20, 30],
    "status": [1, 0, 1]
})

# Updated dataset
df_v2 = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "value": ["10", "25", "30", "40"],
    "category": ["A", "B", None, "C"],
    "amount": [100, 200, 300, 400]
})

diff = data_version_diff(df_v1, df_v2)
display_data_version_diff(diff)  #prints a human-readable summary of the comparison.

# --- resolve string value --
df1 = pd.DataFrame({ "company": ["Google", "Gooogle", "Gogle", "Microsoft", "Microsof"]})
resolve_string_value(df1, "company", ["Google", "Microsoft"], 80)
print(df1)

# --- Generate summary statistics ---
 df = pd.DataFrame({
    'age': [25, 21, 32, None, 40],
    'city': ['NYC', 'LA', 'NYC', 'SF', 'LA']
     })
numeric_stats, categorical_stats = summary_report(df)
print(numeric_stats.head())
print(categorical_stats.head())

# --- load a CSV file with optimized memory usage ---

# If you have a CSV file, simply load it:
df = load_optimized_csv("your_dataset.csv")
print(df.head())
print(df.dtypes)

# Self-contained example (copy-paste to try it out):
import tempfile
import os

sample_data = pd.DataFrame({
    "int8_col": [1, 2, 100, -100, 5],
    "int16_col": [1000, -1000, 30000, -30000, 500],
    "float_col": [1.123, 2.234, 3.345, 4.456, 5.567],
    "sparse_col": [0, 0, 0, 0, 1],       # 80% zeros -> will be sparse
    "category_col": ["A", "A", "B", "B", "C"]  # low cardinality -> categorical
})

with tempfile.TemporaryDirectory() as tmp_dir:
    csv_path = os.path.join(tmp_dir, "sample.csv")
    sample_data.to_csv(csv_path, index=False)

    df_optimized = load_optimized_csv(csv_path)
    print("Optimized dtypes:")
    print(df_optimized.dtypes)
    # int8_col      -> int8 (downcasted)
    # int16_col     -> int16 (downcasted)
    # float_col     -> float32 (downcasted)
    # sparse_col    -> Sparse[int8, 0] (sparse conversion)
    # category_col  -> category (categorical conversion)

```

## Developers

### Development Setup

Clone the repo, create conda environment and register the csvplus environment as a Jupyter kernel.

```bash
git clone https://github.com/UBC-MDS/DSCI_524_group37_csvplus
cd DSCI_524_group37_csvplus

conda env create -f environment.yml
conda activate csvplus

# Optional: register the environment as a Jupyter/Quarto kernel
# (required only if kernel is not registered correctly)
python -m ipykernel install --user --name csvplus --display-name "csvplus"

```

### Install csvplus package (editable mode)

This allows you to edit the source code locally while using the package.

```bash
pip install -e .
```

### Run Tests and Coverage

All tests are written using `pytest`. To run the full test suite and generate a coverage report execute:

```bash
# install coverage tools if not yet installed
pip install pytest pytest-cov

pytest --cov=csvplus --cov-report=term-missing
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
