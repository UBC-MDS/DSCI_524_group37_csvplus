# Welcome to csvplus

|        |        |
|--------|--------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/csvplus-1.svg)](https://pypi.org/project/csvplus-1/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/csvplus-1.svg)](https://pypi.org/project/csvplus-1/)  |
| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |

*TODO: the above badges that indicate python version and package version will only work if your package is on PyPI.
If you don't plan to publish to PyPI, you can remove them.*

csvplus provides a set of convenient enhancements on top of the Python `pandas` package for reading, comparing, cleaning, and summarizing data. Reading CSV files with pandas does not always use the data type of the least memory. Sometimes, it is helpful to tell the differences between two version of a CSV file. Within a CSV file, the file data values can be inconsistent, such as "Google" vs. "Google, Inc.", and they should be treated as the same entity. Also, it is helpful not only to have descriptive statistics, but also the number of missing values.

This package aims to address these pain points with these functions:
|        |        |
|--------|--------|
|load_optimized_csv|Loads a CSV file and automatically downcasts data types to minimize memory footprint.|
|data_version_diff|Compare two versions of a pandas DataFrame and summarize their differences.|
|resolve_string_value|Consolidating spelling variations of the same data value in a column.|
|summary_report|Produce a list of descriptive statistics of the data and information about missing values.|

Our package fits into the Python preprocessing framework. Currently, the [`pandas`](https://pandas.pydata.org/) package provides basic functionality to read CSV and produce summary statistics, and the [`pyjanitor`](https://pyjanitor-devs.github.io/pyjanitor/) package provides functions for sanitizing the column names and converting column dtype. Our package can be used along with these two with more auto-detection and summarization functionalities that further increase the efficiency of data preprocessing and data exploration workflows.

## Contributors
- Alan Liu 
- Oswin Gan
- Purity Jangaya
- Ralah Aaqil

## Get started

You can install this package into your preferred Python environment using pip:

```bash
$ pip install csvplus
```

To use csvplus in your code:

```python
>>> import csvplus
>>> csvplus.load_optimized_csv.load_optimized_csv("large_dataset.csv")
>>> csvplus.data_version_diff.data_version_diff(df_v1, df_v2)
>>> csvplus.data-correction.resolve_string_value(data, "company_name", ["Google", "Microsoft"], 80)
>>> csvplus.generate-report.summary_report(df)
```

## Copyright

- Copyright © 2026 .
- Free software distributed under the [MIT License](./LICENSE).
