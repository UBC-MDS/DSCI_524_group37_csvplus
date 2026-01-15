"""
A module that generates a summary report given an input dataframe.
Includes useful summary statistics for numeric and categorical data
for use in data analysis.

Requires: pandas >= 1.0.0, scipy >= 1.0.0
"""

from typing import Any
import pandas as pd


def summary_report(
    df: pd.DataFrame,
    confidence_level: float = 0.95,
    top_n: int = 5
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    For an input DataFrame, generate a summary report including:

        For numeric columns (int, float):
            - 'count': number of non-null values
            - 'n_missing': number of missing values
            - 'missing_prop': proportion of missing values
            - 'mean': arithmetic mean
            - 'ci_lower': lower bound of confidence interval for mean
            - 'ci_upper': upper bound of confidence interval for mean
            - '50%': median
            - 'std': standard deviation
            - 'min': minimum value
            - '25%': first quartile
            - '75%': third quartile
            - 'max': maximum value
            - 'n_unique': number of unique values

        For categorical columns (object, string, category):
            - 'count': number of non-null values
            - 'n_missing': number of missing values
            - 'missing_prop': proportion of missing values
            - 'n_unique': number of unique values
            - 'unique_prop': proportion of unique values to total count
            - 'is_constant': boolean indicating if only one unique value exists
            - 'top_values': dictionary of {value: count} for up to top_n most frequent values
            - 'top_1_prop': proportion of most common value

    Note: Boolean and datetime columns are treated as categorical.
          Columns with all null values are included with count=0.
          Confidence intervals are calculated using the t-distribution
          and assume approximately normal data or sufficient sample size (n>=30).
          Columns with fewer than 2 non-null values will have ci_lower and
          ci_upper set to None.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to obtain summary statistics for.
    confidence_level : float, default=0.95
        Confidence level for calculating confidence intervals on the mean
        for numeric columns. Must be between 0 and 1 (e.g., 0.95 for 95% CI).
    top_n : int, default=5
        Maximum number of most frequent values to include in top_values
        for categorical columns.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        A tuple of (numeric_stats, categorical_stats) where:
        - numeric_stats: DataFrame with statistics as columns
                         rows are numeric columns indexed by
                         column names from the input DataFrame
        - categorical_stats: DataFrame with statistics as columns
                             rows are categorical columns indexed by
                             column names from the input DataFrame

        If no numeric or categorical columns exist, the respective
        DataFrame will be empty.

    Raises
    ------
    TypeError
        If df is not a pandas.DataFrame.
    ValueError
        If df is empty (has no rows), if confidence_level is not
        between 0 and 1, or if top_n < 1.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'age': [25, 21, 32, None, 40],
    ...     'city': ['NYC', 'LA', 'NYC', 'SF', 'LA']
    ... })
    >>> numeric_stats, categorical_stats = summary_report(df)
    >>> numeric_stats.loc['age', 'mean']
    29.5
    >>> numeric_stats.loc['age', 'n_missing']
    1
    >>> numeric_stats.loc['age', 'missing_prop']
    0.2
    >>> numeric_stats.loc['age', 'ci_lower']
    22.3
    >>> categorical_stats.loc['city', 'n_unique']
    3
    >>> categorical_stats.loc['city', 'top_values']
    {'NYC': 2, 'LA': 2, 'SF': 1}
    >>> categorical_stats.loc['city', 'unique_prop']
    0.6
    """
    # TODO: implement this function
    return None, None
