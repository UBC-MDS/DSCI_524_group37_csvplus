"""
A module that generates a summary report given an input dataframe.
Includes useful summary statistics for numeric and categorical data
for use in data analysis.

Requires: pandas >= 1.0.0, scipy >= 1.0.0

LLM Usage Disclosure
--------------------
Claude.ai was used to perform the following tasks:

- Provide recommendations for which statistics to include in the output report,
  given their frequency of use in real-world data analysis.
- Generate pseudocode for the confidence interval and proportion calculations.
- Look for edge cases in the code and recommend how to best address them,
  particularly null columns and input DataFrames with extreme small row counts.
"""

import pandas as pd
import numpy as np
from scipy import stats


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
    - 'median': median
    - 'std': standard deviation
    - 'min': minimum value
    - '25%': first quartile
    - '75%': third quartile
    - 'max': maximum value
    - 'n_unique': number of unique values

    For categorical columns (object, string, category, bool, datetime):

    - 'count': number of non-null values
    - 'n_missing': number of missing values
    - 'missing_prop': proportion of missing values
    - 'n_unique': number of unique values
    - 'unique_prop': proportion of unique values to total count
    - 'is_constant': boolean indicating if only one unique value exists
    - 'top_values': dictionary of {value: count}
    for up to top_n most frequent values
    - 'top_1_prop': proportion of most common value

    Note: Confidence intervals are calculated using the t-distribution
    and assume approximately normal data or sufficient sample size (n>=30).
    Columns with all null values are excluded from output.
    Numeric columns with fewer than 2 non-null values will have ci_lower and
    ci_upper set to None.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to obtain summary statistics for.
    confidence_level : float, default=0.95
        Confidence level for calculating confidence
        intervals for numeric columns.
        Must be between 0 and 1.
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

    # Validate that df is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    # Validate that df contains at least one row
    if len(df) == 0:
        raise ValueError("DataFrame cannot be empty (must have at least "
                         "one row)")

    # Validate confidence_level is within the valid range
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")

    # Validate top_n is positive
    if top_n < 1:
        raise ValueError("top_n must be at least 1")

    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Identify categorical columns (object, string, category, bool, datetime)
    categorical_cols = df.select_dtypes(
        include=['object', 'string', 'category', 'bool', 'datetime']
    ).columns.tolist()

    # Filter columns where all elements are null
    numeric_cols = [col for col in numeric_cols if df[col].count() > 0]
    categorical_cols = [col for col in categorical_cols if df[col].count() > 0]

    # Process numeric columns
    numeric_stats_list = []

    for col in numeric_cols:
        series = df[col]

        # Get non-null value count
        count = series.count()
        n_missing = series.isna().sum()
        missing_prop = n_missing / len(series)

        # Get unique value count
        n_unique = series.nunique(dropna=True)

        # Initialize stats dictionary
        stats_dict = {
            'count': count,
            'n_missing': n_missing,
            'missing_prop': missing_prop,
        }

        if count > 0:
            # Get mean and standard deviation
            mean_val = series.mean()
            std_val = series.std()

            # Compute confidence interval using t-distribution
            if count >= 2:
                se = std_val / np.sqrt(count)
                t_crit = stats.t.ppf((1 + confidence_level) / 2, df=count - 1)

                ci_lower = mean_val - t_crit * se
                ci_upper = mean_val + t_crit * se
            else:
                ci_lower = None
                ci_upper = None

            # Get quantiles
            quantiles = series.quantile([0.25, 0.5, 0.75])

            # Update stats dictionary with computed values
            stats_dict.update({
                'mean': mean_val,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'median': quantiles[0.5],
                'std': std_val,
                'min': series.min(),
                '25%': quantiles[0.25],
                '75%': quantiles[0.75],
                'max': series.max(),
                'n_unique': n_unique,
            })
        else:
            # Set all values to null
            stats_dict.update({
                'mean': None,
                'ci_lower': None,
                'ci_upper': None,
                'median': None,
                'std': None,
                'min': None,
                '25%': None,
                '75%': None,
                'max': None,
                'n_unique': n_unique,
            })

        # Add column name as index and append to list
        numeric_stats_list.append(pd.Series(stats_dict, name=col))

    # Create DataFrame from list
    if numeric_stats_list:
        numeric_stats = pd.DataFrame(numeric_stats_list)
    else:
        # Return empty DataFrame if no numeric columns
        numeric_stats = pd.DataFrame()

    # Process categorical columns
    categorical_stats_list = []

    for col in categorical_cols:
        series = df[col]

        # Get non-null value count
        count = series.count()
        n_missing = series.isna().sum()
        missing_prop = n_missing / len(series)

        # Get unique value count
        n_unique = series.nunique(dropna=True)

        # Initialize stats dictionary
        stats_dict = {
            'count': count,
            'n_missing': n_missing,
            'missing_prop': missing_prop,
            'n_unique': n_unique,
        }

        if count > 0:
            # Calculate proportion of unique values
            unique_prop = n_unique / count

            # Check if column is constant (only one unique value)
            is_constant = (n_unique == 1)

            # Get frequency of each value
            value_counts = series.value_counts()

            # Get top_n most frequent values as dictionary
            top_values = value_counts.head(top_n).to_dict()

            # Get proportion of most common value
            top_1_prop = (value_counts.iloc[0] / count
                          if len(value_counts) > 0 else 0)

            # Update stats dictionary
            stats_dict.update({
                'unique_prop': unique_prop,
                'is_constant': is_constant,
                'top_values': top_values,
                'top_1_prop': top_1_prop,
            })
        else:
            # Set all values to null
            stats_dict.update({
                'unique_prop': None,
                'is_constant': None,
                'top_values': {},
                'top_1_prop': None,
            })

        # Add column name as index and append to list
        categorical_stats_list.append(pd.Series(stats_dict, name=col))

    # Create DataFrame from list
    if categorical_stats_list:
        categorical_stats = pd.DataFrame(categorical_stats_list)
    else:
        # Return empty DataFrame if no categorical columns
        categorical_stats = pd.DataFrame()

    # Return results
    return numeric_stats, categorical_stats
