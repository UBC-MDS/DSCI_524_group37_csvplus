"""
A module that replaced data values to the resolved name within a column.
Requires `pandas` and `rapidfuzz`.
"""


from pandas.api.types import is_string_dtype
from rapidfuzz import process, fuzz


def resolve_string_value(df, column_name, resolved_names, threshold):
    """
    For all the values in the column_name of the df, find the one element
    in the `resolved_names` with highest
    similarity score computed with `fuzz.WRatio`
    (case sensitive, meaning that "Google" and
    "google" will not have a score of 100).
    And compare the similiarty score with
    the threshold to decide whether to apply
    the string replacement inplace.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame of interest.
    column_name : str
        The column to conduct the consolidation on.
        The column must exist in `df` and
        be of type string.
    resolved_names : list
        A list of standard names for transforming the column's value to.
    threshold: float
        The minimum similarity score (0 and 100) required to replace
        a value with a resolved name.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If column_name is not in df.
        If resolved_names is empty.
        If threshold is below 0 or above 100.
    TypeError
        If df[column_name] dtype is not string.

    Examples
    --------
    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...     "company_name": ["Google", "Google Inc.",
    ...     "Gogle", "Microsoftt", "Micro-soft"],
    ...     "num_searches": [1, 2, 3, 4, 5]
    ... })
    >>> resolve_string_value(data, "company_name", ["Google", "Microsoft"], 80)
    >>> print(data)
       company_name  num_searches
    0   Google       1
    1   Google       2
    2   Google       3
    3   Microsoft    4
    4   Microsoft    5
    """
    # checks
    if column_name not in df.columns:
        raise ValueError("The given column_name does not exist.")
    elif not is_string_dtype(df[column_name]):
        raise TypeError("The column is not of type string.")
    elif not resolved_names:
        raise ValueError("The given resolved_names is empty.")
    elif (threshold < 0) or (threshold > 100):
        raise ValueError("The threshold value is out of range.")

    # Adopted MS Copilot solution to:
    # "How to use `rapidfuzz.process.extractOne()`"?"
    # Return closest string in `choices` if similarity score based on
    # `fuzz.WRatio` is
    # above threshold. Otherwise, return the word itself.
    def find_closest(query, choices, threshold):
        result = process.extractOne(query, choices, scorer=fuzz.WRatio)
        if result and result[1] >= threshold:
            return result[0]
        else:
            return query

    df[column_name] = (df[column_name].apply(
        lambda x: find_closest(x, resolved_names, threshold)))
