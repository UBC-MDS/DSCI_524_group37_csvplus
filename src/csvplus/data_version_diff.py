"""
Summarize structural and statistical differences between two DataFrames.
"""
import pandas as pd


def data_version_diff(df_v1, df_v2):
    """
    This function compares an earlier and a later version of a pandas
    DataFrame and returns a high-level summary of how the data has changed.
    It is designed for data auditing, version tracking, and exploratory
    analysis rather than cell-by-cell comparison.

    The comparison includes:
    - Columns that were added or removed
    - Changes in row counts
    - Changes in missing values by column
    - Changes in summary statistics for numeric columns
    - Changes in data types

    Parameters
    ----------
    df_v1 : pandas.DataFrame
        The original or earlier version of the dataset.

    df_v2 : pandas.DataFrame
        The updated or later version of the dataset.

    Returns
    -------
    diff: dict
        A dictionary summarizing differences between the two DataFrames.

    Notes
    -----
    - This function assumes both inputs are pandas DataFrames.
    - Rows are compared by position only; no key-based row matching is
      performed.
    - The function is intended for small to medium-sized datasets and
      exploratory analysis rather than large-scale production pipelines.

    Examples
    --------
    >>> import pandas as pd
    >>> from csvplus.data_version_diff import data_version_diff
    >>>
    >>> # Original dataset
    >>> df_v1 = pd.DataFrame({
    ...     "id": [1, 2, 3],
    ...     "value": [10, 20, 30],
    ...     "status": [1, 0, 1]
    ... })
    >>>
    >>> # Updated dataset
    >>> df_v2 = pd.DataFrame({
    ...     "id": [1, 2, 3, 4],
    ...     "value": ["10", "25", "30", "40"],
    ...     "category": ["A", "B", None, "C"],
    ...     "amount": [100, 200, 300, 400]
    ... })
    >>>
    >>> # Compare the two DataFrames
    >>> diff = data_version_diff(df_v1, df_v2)
    >>>
    >>> # Check which columns were added
    >>> diff["columns_added"]
    >>>
    >>> # Check which columns were removed
    >>> diff["columns_removed"]
    >>>
    >>> # Row count change
    >>> diff["row_count_change"]
    >>>
    >>> # Missing value changes
    >>> diff["missing_value_changes"]
    >>>
    >>> # Numeric summary changes
    >>> diff["numeric_summary_changes"]
    """

    # get column name sets
    old_cols = set(df_v1.columns)
    new_cols = set(df_v2.columns)

    # columns added and removed
    columns_added = sorted(new_cols - old_cols)
    columns_removed = sorted(old_cols - new_cols)

    # row_count_change
    old_row_count = len(df_v1)
    new_row_count = len(df_v2)
    row_difference = new_row_count - old_row_count

    # missing_value_changes
    shared_columns = df_v1.columns.intersection(df_v2.columns)  # shared cols
    missing_summary = pd.DataFrame({
        "missing_old": df_v1[shared_columns].isna().sum(),
        "missing_new": df_v2[shared_columns].isna().sum()
    })

    # calculate the difference
    missing_summary["difference"] = (
        missing_summary["missing_new"] - missing_summary["missing_old"]
    )

    # reset index so 'column' is a regular column
    missing_summary = (
        missing_summary.reset_index().rename(columns={"index": "column"})
    )

    # print(f"Missing value summary: {missing_summary}")

    # numeric_summary_changes
    # identify numeric cols in both DFs
    numeric_cols_old = df_v1.select_dtypes(include="number").columns
    numeric_cols_new = df_v2.select_dtypes(include="number").columns
    shared_numeric_columns = numeric_cols_old.intersection(numeric_cols_new)

    # compute summary statistics for shared numeric columns
    if len(shared_numeric_columns) == 0:
        numeric_summary_changes = pd.DataFrame(
            columns=["column", "statistic", "old", "new", "difference"]
        )
    else:
        summary_old = (
            df_v1[shared_numeric_columns].describe()
            .loc[['mean', 'std', 'min', 'max']].T
        )
        summary_new = (
            df_v2[shared_numeric_columns].describe()
            .loc[['mean', 'std', 'min', 'max']].T
        )

        # convert to long format
        summary_old_long = (
            summary_old.reset_index()
            .melt(id_vars="index", var_name="statistic", value_name="old")
            .rename(columns={"index": "column"})
        )

        summary_new_long = (
            summary_new.reset_index()
            .melt(id_vars="index", var_name="statistic", value_name="new")
            .rename(columns={"index": "column"})
        )

        # merge old and new
        numeric_summary_changes = summary_old_long.merge(
            summary_new_long, on=["column", "statistic"], how="inner"
        )

        # calculate the difference
        numeric_summary_changes["difference"] = (
            numeric_summary_changes["new"] - numeric_summary_changes["old"]
        )

    # --- dtype_changes ---
    # for each shared column, compare types
    dtype_changes_list = []
    for col in shared_columns:
        old_type = df_v1[col].dtype
        new_type = df_v2[col].dtype
        if old_type != new_type:
            dtype_changes_list.append({
                "column": col, "old_dtype": str(old_type),
                "new_type": str(new_type)
                })

    # convert to DF
    dtype_changes = pd.DataFrame(dtype_changes_list)

    diff = {
        "columns_added": columns_added,
        "columns_removed": columns_removed,
        "row_count_change": {
            "old_row_count": old_row_count,
            "new_row_count": new_row_count,
            "row_difference": row_difference
        },
        "missing_value_changes": missing_summary,
        "numeric_summary_changes": numeric_summary_changes,
        "dtype_changes": dtype_changes,
        "summary": {
            "n_columns_added": len(columns_added),
            "n_columns_removed": len(columns_removed),
            "n_dtype_changes": len(dtype_changes),
            "n_missing_changes": int(
                (missing_summary["difference"] != 0).sum()
            ),
        },
    }

    return diff


def display_data_version_diff(diff):
    """
    Print a formatted, human-readable summary of DataFrame version differences.

    This function takes the output of `data_version_diff` and prints a
    structured console report highlighting row count changes, schema changes,
    missing value differences, numeric summary changes, and data type changes.

    Parameters
    ----------
    diff : dict
        The dictionary returned by `data_version_diff`.

    Notes
    -----
    - This function is intended for interactive use (e.g., notebooks or
      terminals).
    - It does not return any value.

    Examples
    --------
    >>> import pandas as pd
    >>> from csvplus.data_version_diff import display_data_version_diff
    >>>
    >>> diff = data_version_diff(df_v1, df_v2)
    >>> display_data_version_diff(diff)
    """
    print("\n" + "=" * 60)
    print("DATA VERSION CHANGE SUMMARY")
    print("=" * 60)

    # --- Row count ---
    rc = diff["row_count_change"]
    row_diff = rc["row_difference"]
    sign = "+" if row_diff > 0 else ""
    print("\n  ROWS CHANGE:")
    print("-" * 60)
    print(f"    Old Rows: {rc['old_row_count']}")
    print(f"    New Rows: {rc['new_row_count']}")
    print(f"    Change: {sign}{row_diff}")

    # --- Columns added / removed ---
    print("\n   SCHEMA CHANGES:")
    print("-" * 60)
    if diff["columns_added"]:
        print(f"    Columns added: {', '.join(diff['columns_added'])}")
    else:
        print(" Columns added: None")

    if diff["columns_removed"]:
        print(f"    Columns removed: {', '.join(diff['columns_removed'])}")
    else:
        print(" Columns removed: None")

    # --- Missing values ---
    mv = diff["missing_value_changes"]
    mv_changed = mv[mv["difference"] != 0]

    print("\n   MISSING VALUE CHANGES:")
    print("-" * 60)
    if mv_changed.empty:
        print(" No changes in missing values.")
    else:
        print(
            mv_changed.assign(
                change=lambda d: d["difference"].apply(
                    lambda x: f"+{x}" if x > 0 else str(x)
                )
            )[["column", "missing_old", "missing_new", "change"]]
            .to_string(index=False)
        )

    # --- Numeric summary changes ---
    ns = diff["numeric_summary_changes"]
    ns_changed = ns[ns["difference"] != 0]

    print("\n   NUMERIC SUMMARY CHANGES:")
    print("-" * 60)
    if ns_changed.empty:
        print(" No numeric summary changes.")
    else:
        print(ns_changed.round(2).to_string(index=False))

    # --- Dtype changes ---
    dt = diff["dtype_changes"]
    print("\n   DATA TYPE CHANGES:")
    print("-" * 60)
    if dt.empty:
        print(" No data type changes.")
    else:
        print(dt.to_string(index=False))
