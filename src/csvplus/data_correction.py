"""
A module that consolidates similar data values to the standard (resolved) name within a column.
"""

def resolve_string_value(df, column_name, resolved_names, threshold):
    """
    For all the values in the column_name of the df, check if there is a standard version
    in the `resolved_names` (computing a similarity score and using the threshold to determine),
    and apply the string replacement inplace.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame of interest.
    column_name : str
        The column to conduct the consolidation on.
    resolved_names : list
        A list of standard names for transforming the column's value to.
    threshold: int
        the value used for determining if the matched value in `resolved_names` is similar enough.

    Returns
    -------
    None

    Examples
    --------
    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...     "company_name": ["Google", "Google Inc.", "Gogle", "Microsoftt", "Micro-soft"],
    ...     "location": ["Mt. view", "Mt. view", "Mt. view", "Redmond", , "Redmond"]
    ... })
    >>> resolve_string_value(data, "company_name", ["Google", "Microsoft"], 80)
    >>> data
       company_name  location
    1   Google       Mt. view
    2   Google       Mt. view
    3   Google       Mt. view
    4   Microsoft    Redmond
    5   Microsoft    Redmond
    """
    # TODO: implement this function
    return None
