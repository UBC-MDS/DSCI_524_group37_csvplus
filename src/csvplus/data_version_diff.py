import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
Faker.seed(123)
np.random.seed(123)

def data_version_diff(df_old, df_new):
    """
    Compare two versions of a pandas DataFrame and summarize their differences.

    This function is intended to support data auditing, reproducibility, and
    exploratory analysis by identifying structural and statistical differences
    between two versions of a dataset. Rather than performing a cell-by-cell
    comparison, the function provides a high-level summary of how the datasets
    differ.

    The comparison includes:
    - Columns that were added or removed
    - Changes in row counts
    - Changes in missing values by column
    - Changes in summary statistics for numeric columns
    - Changes in data types

    Parameters
    ----------
    df_old : pandas.DataFrame
        The original or earlier version of the dataset.

    df_new : pandas.DataFrame
        The updated or later version of the dataset.

    Returns
    -------
    dict
        A dictionary summarizing the differences between the two DataFrames with
        the following keys:

        - 'columns_added' : list of str
            Column names present in `df_new` but not in `df_old`.

        - 'columns_removed' : list of str
            Column names present in `df_old` but not in `df_new`.

        - 'row_count_change' : dict
            A dictionary with keys:
                - 'old' : int
                    Number of rows in `df_old`.
                - 'new' : int
                    Number of rows in `df_new`.
                - 'difference' : int
                    Difference in row counts (`new - old`).

        - 'missing_value_changes' : pandas.DataFrame
            A DataFrame summarizing changes in missing value counts for columns
            present in both datasets.

        - 'numeric_summary_changes' : pandas.DataFrame
            A DataFrame summarizing changes in summary statistics (e.g., mean,
            standard deviation, minimum, maximum) for numeric columns present
            in both datasets.

        - 'dtype_changes' : pandas.DataFrame
            A DataFrame listing columns whose data types differ between
            `df_old` and `df_new`.

    Notes
    -----
    - This function assumes both inputs are pandas DataFrames.
    - Rows are compared by position only; no key-based row matching is performed.
    - The function is intended for small to medium-sized datasets and exploratory
      analysis rather than large-scale production pipelines.

    Examples
    --------
    >>> diff = data_version_diff(df_v1, df_v2)
    >>> diff["columns_added"]
    ['new_feature']

    >>> diff["row_count_change"]["difference"]
    150
    """

    # get column name sets
    old_cols = set(df_old.columns)
    new_cols = set(df_new.columns)

    #columns added and removed
    columns_added = list(new_cols - old_cols)
    columns_removed = list(old_cols - new_cols)

    #row_count_change
    old_row_count = len(df_old)
    new_row_count = len(df_new)
    row_difference = new_row_count - old_row_count

    #missing_value_changes
    shared_columns = df_old.columns.intersection(df_new.columns) #shared columns
    missing_summary = pd.DataFrame({
        "missing_old": df_old[shared_columns].isna().sum(),
        "missing_new": df_new[shared_columns].isna().sum()
    })

    #calculate the difference
    missing_summary["difference"] = missing_summary["missing_new"] - missing_summary["missing_old"]

    #reset index so 'column' is a regular column
    missing_summary = missing_summary.reset_index().rename(columns={"index": "column"})

    #print(f"Missing value summary: {missing_summary}")

    ## numeric_summary_changes
    #identify numeric cols in both DFs
    numeric_cols_old = df_old.select_dtypes(include="number").columns
    numeric_cols_new = df_new.select_dtypes(include="number").columns
    shared_numeric_columns = numeric_cols_old.intersection(numeric_cols_new) 

    #compute summary statistics for shared numeric columns
    summary_old = df_old[shared_numeric_columns].describe().loc[['mean', 'std', 'min', 'max']].T
    summary_new = df_new[shared_numeric_columns].describe().loc[['mean', 'std', 'min', 'max']].T

    # convert to long format
    summary_old_long = summary_old.reset_index().melt(id_vars="index", var_name="statistic", value_name="old").rename(columns={"index": "column"})

    summary_new_long = summary_new.reset_index().melt(
    id_vars="index", var_name="statistic", value_name="new"
    ).rename(columns={"index": "column"})

    # merge old and new 
    numeric_summary_changes = summary_old_long.merge(
        summary_new_long, on=["column", "statistic"], how="inner"
    )

    # calculate the difference
    numeric_summary_changes["difference"] = (
        numeric_summary_changes["new"] - numeric_summary_changes["old"]
    )

    ###### dtype_changes ##############
    #for each shared column, compare types
    dtype_changes_list = []
    for col in shared_columns:
        old_type = df_old[col].dtype
        new_type = df_new[col].dtype
        if old_type != new_type:
            dtype_changes_list.append({"column": col, "old_dtype": old_type, "new_type": new_type})

    #convert to DF
    dtype_changes = pd.DataFrame(dtype_changes_list)

    result = {
        "columns_added": columns_added,
        "columns_removed": columns_removed,
        "row_count_change": {
            "old_row_count": old_row_count,
            "new_row_count": new_row_count,
            "row_difference": row_difference
        },
        "missing_value_changes": missing_summary,
        "numeric_summary_changes": numeric_summary_changes,
        "dtype_changes": dtype_changes
    }

    return result

"""
####### TESTING USING DUMMY DATA #################
"""

n_old = 100

df_old = pd.DataFrame({
    "user_id": range(1, n_old + 1),
    "age": np.random.randint(18, 70, size=n_old),
    "income": np.random.normal(loc=5000, scale=15000, size=n_old),
    "email": [fake.email() for _ in range(n_old)],
    "signup_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(n_old)],
    "country": [fake.country() for _ in range(n_old)],
})

#introduce missing values in df_old
age_missing_idx = np.random.choice(df_old.index, size=10, replace=False)
df_old.loc[age_missing_idx, "age"] = np.nan

email_missing_idx = np.random.choice(df_old.index, size=3, replace=False)
df_old.loc[email_missing_idx, "email"] = np.nan

#create df_new
df_new = df_old.copy()

#add rows for row count change
n_new_rows = 20

new_rows = pd.DataFrame({
    "user_id": range(df_old["user_id"].max() + 1, df_old["user_id"].max() + 1 + n_new_rows),
    "age": np.random.randint(18, 70, size=n_new_rows),
    "income": np.random.normal(loc=60000, scale=20000, size=n_new_rows),
    "email": [fake.email() for _ in range(n_new_rows)],
    "signup_date": [fake.date_between(start_date="-1y", end_date="today") for _ in range(n_new_rows)],
    "country": [fake.country() for _ in range(n_new_rows)],
})
df_new = pd.concat([df_new, new_rows], ignore_index=True)

#column removal
df_new = df_new.drop(columns=["country"])

#column addition
df_new["last_login_date"] = [
    fake.date_between(start_date="-6m", end_date="today") for _ in range(len(df_new))
]

## missing value changes
#reduce missing ages (fill some)
df_new['age'] = df_new['age'].fillna(df_new['age'].median())

#introduce missing income values
income_missing_idx = np.random.choice(df_new.index, size=8, replace=False)
df_new.loc[income_missing_idx, "income"] = np.nan

## data type change
df_new["age"] = df_new["age"].astype(str)

## sanity checks
# df_old.info()
# df_new.info()

# df_old.head()
# df_new.head()

#result = data_version_diff(df_old, df_new)

def display_data_version_diff(result):
    print("\n" + "=" * 60)
    print("DATA VERSION CHANGE SUMMARY")
    print("=" * 60)

    # --- Row count ---
    rc = result["row_count_change"]
    diff = rc["row_difference"]
    sign = "+" if diff > 0 else ""
    print(f"\n  ROWS CHANGE:")
    print("-" * 60)
    print(f"    Old Rows: {rc['old_row_count']}")
    print(f"    New Rows: {rc['new_row_count']}")
    print(f"    Change: {sign}{diff}")

    # --- Columns added / removed ---
    print("\n   SCHEMA CHANGES:")
    print("-" * 60)
    if result["columns_added"]:
        print(f"    Columns added: {', '.join(result['columns_added'])}")
    else:
        print(" Columns added: None")
    
    if result["columns_removed"]:
        print(f"    Columns removed: {', '.join(result['columns_removed'])}")
    else:
        print(" Columns removed: None")

    # --- Missing values ---
    mv = result["missing_value_changes"]
    mv_changed = mv[mv["difference"] != 0]
    
    print("\n   MISSING VALUE CHANGES:")
    print("-" * 60)
    if mv_changed.empty:
        print(" No changes in missing values.")
    else:
        print(
            mv_changed.assign(
                change=lambda d: d["difference"].apply(
                    lambda x: f"+{x}" if x>0 else str(x)
                )
            )[["column", "missing_old", "missing_new", "change"]]
            .to_string(index=False)
        )
    
    # --- Numeric summary changes ---
    ns = result["numeric_summary_changes"]
    ns_changed = ns[ns["difference"] != 0]

    print("\n   NUMERIC SUMMARY CHANGES:")
    print("-" * 60)
    if ns_changed.empty:
        print(" No numeric summary changes.")
    else:
        print(ns_changed.round(2).to_string(index=False))

    # --- Dtype changes ---
    dt = result["dtype_changes"]
    print("\n   DATA TYPE CHANGES:")
    print("-" * 60)
    if dt.empty:
        print(" No data type changes.")
    else:
        print(dt.to_string(index=False))

result = data_version_diff(df_old, df_new)
display_data_version_diff(result)
