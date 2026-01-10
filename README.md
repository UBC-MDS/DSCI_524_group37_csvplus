# Welcome to csvplus

|        |        |
|--------|--------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/csvplus-1.svg)](https://pypi.org/project/csvplus-1/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/csvplus-1.svg)](https://pypi.org/project/csvplus-1/)  |
| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |

*TODO: the above badges that indicate python version and package version will only work if your package is on PyPI.
If you don't plan to publish to PyPI, you can remove them.*

csvplus provides a set of convenient enhancements on top of the Python `pandas` package for reading, cleaning, and summarizing data. Working with CSV files in pandas often requires manually specifying encodings or column types, which can be tedious. During analysis, it is common to encounter inconsistent values, such as "Google" vs. "Google, Inc.", that should be treated as the same entity. During data exploration, pandas offers descriptive statistics, but it does not automatically generate visual summaries.

This package aims to address these pain points with these functions:
|        |        |
|--------|--------|
|read_csv_auto|Automatically detecting the correct encoding when reading CSV files|
|detect_column_types|Inferring appropriate data types for each column|
|consolidate_data_variation|Consolidating variations of the same data value|
|summary_report|Producing graphical summary reports of the dataset|

Our package fits into the Python preprocessing framework. Currently, the [`pandas`](https://pandas.pydata.org/) package provides basic functionality to read CSV and detect NA values, and the [`pyjanitor`](https://pyjanitor-devs.github.io/pyjanitor/) package sanitizes the column names, convert column dtype to categorical, and add onto dealing with missing data functionalities. Our package builds on top of those two with auto-detection capacities that further simplify data import, cleaning, and exploration, so that the data scientist can focus on modeling.

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

TODO: Add a brief example of how to use the package to this section

To use csvplus in your code:

```python
>>> import csvplus
>>> csvplus.hello_world()
```

## Copyright

- Copyright © 2026 .
- Free software distributed under the [MIT License](./LICENSE).
