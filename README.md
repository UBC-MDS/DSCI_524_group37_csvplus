# csvplus

|        |        |
|--------|--------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/csvplus-1.svg)](https://pypi.org/project/csvplus-1/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/csvplus-1.svg)](https://pypi.org/project/csvplus-1/)  |
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

---

## Get started

### Installation

You can install the package into your preferred Python environment in editable mode (recommended for development):

```bash
git clone git@github.com:UBC-MDS/DSCI_524_group37_csvplus.git csvplus
cd csvplus
pip install -e .
```

Or install via pip (once published):

```bash
pip install csvplus
```

### Usage

To use csvplus in your code:

```python
from csvplus.data_version_diff import data_version_diff, display_data_version_diff
from csvplus.load_optimized_csv import load_optimized_csv
from csvplus.data_correction import resolve_string_value
from csvplus.generate_report import summary_report

# --- test data type change in csvplus.data_version_diff ---
df1 = pd.DataFrame({"a": [1,2,3]})
df2 = pd.DataFrame({"a": ["1","2","3"]})
diff = data_version_diff(df1, df2)
print(diff)
# Optionally display a formatted summary
display_data_version_diff(diff)

# --- csvplus.data_correction --
df_v1 = load_optimized_csv("large_dataset.csv")
df_v2 = load_optimized_csv("large_dataset2.csv")
resolve_string_value(df1, "company_name", ["Google", "Microsoft"], 80)
summary_report(df1)
```

### Running Tests

All tests are written using `pytest`

To run the full test suite, navigate to the project root directory and execute:

```bash
pytest
```

This will automatically discover and run all tests in the `tests/` folder.

## Contributors

- Alan Liu
- Oswin Gan
- Purity Jangaya
- Ralah Aaqil

## License

- Copyright © 2026
- Free software distributed under the [MIT License](./LICENSE).
