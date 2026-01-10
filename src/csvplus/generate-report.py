"""
A module that generates a summary report given an input dataframe.
"""

def summary_report(df):
    """
    For an input DataFrame, generate a summary report including:
        For numeric columns:
            - 'count': number of non-null values
            - 'mean': arithmetic mean
            - 'std': standard deviation
            - 'min': minimum value
            - 'max': maximum value
            - '25%': first quartile
            - '50%': median
            - '75%': third quartile
            - 'missing': number of missing values
            - 'n_unique': number of unique values
        For categorical columns:
            - 'count': number of non-null values
            - 'mode': list of most frequent values
            - 'missing': number of missing values
            - 'n_unique': number of unique values

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to obtain summary statistics for.

    Returns
    -------
    dict
        Dictionary consisting of two keys:
        - 'numeric': dict {column_name: summary_stat} for numeric columns
        - 'categorical': dict {column_name: summary_stat} for categorical columns

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'age': [25, 21, 32, None, 40],
    ...     'city': ['NYC', 'LA', 'NYC', 'SF', 'LA']
    ... })
    >>> stats = summarize_dataframe(df)
    >>> stats['numeric']['age']['mean']
    29.5
    >>> stats['categorical']['city']['mode']
    ['NYC', 'LA']
    """
    # TODO: implement this function
    return None
