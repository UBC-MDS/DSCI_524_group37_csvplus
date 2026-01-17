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
pip install -e .
```

Or install via pip (once published):

```bash
pip install csvplus
```

### Usage

To use csvplus in your code:

```python
>>> import csvplus
>>> csvplus.load_optimized_csv.load_optimized_csv("large_dataset.csv")
>>> csvplus.data_version_diff.data_version_diff(df_v1, df_v2)
>>> csvplus.data-correction.resolve_string_value(data, "company_name", ["Google", "Microsoft"], 80)
>>> csvplus.generate-report.summary_report(df)
```

1. Compare two versions of a dataset - `data_version_diff`

The `data_version_diff` function lets you compare two `pandas.DataFrame` objects and get a high-level summary of the differences, including:

- Columns added or removed
- Changes in row counts
- Missing value changes
- Numeric summary changes
- Data type changes

You can also use the `display_data_version_diff` function to print a readable summary in the console.

```python
from csvplus.data_version_diff import data_version_diff, display_data_version_diff

# Compare two DataFrames
diff = data_version_diff(df_v1, df_v2)

# Inspect the returned dictionary
print(diff["columns_added"])
print(diff["row_count_change"])

# Optionally display a formatted summary
display_data_version_diff(diff)
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
