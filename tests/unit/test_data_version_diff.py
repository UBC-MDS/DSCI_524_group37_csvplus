import pandas as pd
import pytest

from csvplus.data_version_diff import data_version_diff

# test: function returns expected keys
def test_data_version_diff_returns_expected_keys():
    """
    Ensure the function returns a dictionary with all expected top-level keys.
    """

    df_old = pd.DataFrame({"a": [1, 2]})
    df_new = pd.DataFrame({"a": [1,2]})

    result = data_version_diff(df_old, df_new)

    expected_keys = {
        "columns_added",
        "columns_removed",
        "row_count_change",
        "missing_value_changes",
        "numeric_summary_changes",
        "dtype_changes",
        "summary",
    }

    assert isinstance(result, dict)
    assert expected_keys.issubset(result.keys())

# test: columns added and removed 
def test_columns_added_and_removed():
    """
    Verify that added and removed columns are correctly identified.
    """

    df_old = pd.DataFrame({"a": [1], "b": [2]})
    df_new = pd.DataFrame({"b": [2], "c": [3]})

    result = data_version_diff(df_old, df_new)

    assert result["columns_added"] == ["c"]
    assert result["columns_removed"] == ["a"]

# test: row count change
def test_row_count_change():
    """
    Check that row count differences are computed correctly.
    """

    df_old = pd.DataFrame({"a": [1,2,3]})
    df_new = pd.DataFrame({"a": [1,2,3,4,5]})

    result = data_version_diff(df_old, df_new)

    assert result["row_count_change"]["old_row_count"] == 3
    assert result["row_count_change"]["new_row_count"] == 5
    assert result["row_count_change"]["row_difference"] == 2

# test: missing value change
def test_missing_value_changes():
    """
    Confirm that changes in missing values per column are correctly summarized.
    """

    df_old = pd.DataFrame({"a": [1, None, 3]})
    df_new = pd.DataFrame({"a": [1, 2, 3]})

    result = data_version_diff(df_old, df_new)
    mv = result["missing_value_changes"]

    row = mv.loc[mv["column"] == "a"].iloc[0]

    assert row["missing_old"] == 1
    assert row["missing_new"] == 0
    assert row["difference"] == -1

# test: no shared numeric columns (branch coverage)
def test_numeric_summary_no_shared_numeric_columns():
    """
    Ensure an empty numeric summary is returned when no shared numeric columns exist.
    """

    df_old = pd.DataFrame({"a": ["x", "y"]})
    df_new = pd.DataFrame({"a": ["z", "w"]})

    result = data_version_diff(df_old, df_new)
    numeric_summary = result["numeric_summary_changes"]

    assert isinstance(numeric_summary, pd.DataFrame)
    assert numeric_summary.empty
    assert list(numeric_summary.columns) == [
        "column", "statistic", "old", "new", "difference"
    ]

# test: summary reports no missing changes
def test_summary_no_missing_changes():
    """
    Verify the summary correctly reports zero missing-value changes.
    """

    df_old = pd.DataFrame({"a": [1, 2, 3]})
    df_new = pd.DataFrame({"a": [4, 5, 6]})

    result = data_version_diff(df_old, df_new)

    assert result["summary"]["n_missing_changes"] == 0

# test: dtype changes detected
def test_dtype_changes_detected():
    """
    Check that data type changes between versions are detected.
    """

    df_old = pd.DataFrame({"a": [1, 2, 3]})
    df_new = pd.DataFrame({"a": ["1", "2", "3"]})

    result = data_version_diff(df_old, df_new)
    dtype_changes = result["dtype_changes"]

    assert len(dtype_changes) == 1
    assert dtype_changes.iloc[0]["column"] == "a"

def test_numeric_summary_changes_computed_correctly():
    """
    Ensure numeric summary differences are correctly calculated for shared numeric columns.
    """

    df_old = pd.DataFrame({"a": [1, 2, 3]})
    df_new = pd.DataFrame({"a": [2, 3, 4]})  # all numbers increased by 1

    result = data_version_diff(df_old, df_new)
    numeric_summary = result["numeric_summary_changes"]

    # Extract differences per statistic
    diff_dict = dict(zip(numeric_summary["statistic"], numeric_summary["difference"]))

    # min, max, mean should each increase by 1
    assert diff_dict["min"] == 1
    assert diff_dict["max"] == 1
    assert diff_dict["mean"] == 1

    # std difference should be 0 (no change)
    assert diff_dict["std"] == 0

def test_multiple_columns_added():
    """
    Verify that multiple added columns are correctly reported.
    """

    df_old = pd.DataFrame({"a": [1]})
    df_new = pd.DataFrame({"a": [1], "b": [2], "c": [3]})

    result = data_version_diff(df_old, df_new)

    assert sorted(result["columns_added"]) == ["b", "c"]
    assert result["columns_removed"] == []


# test: empty dataframes
def test_empty_dataframes():
    """
    Ensure the function handles empty DataFrames without error.
    """

    df_old = pd.DataFrame()
    df_new = pd.DataFrame()

    result = data_version_diff(df_old, df_new)

    assert result["row_count_change"]["old_row_count"] == 0
    assert result["row_count_change"]["new_row_count"] == 0
    assert result["columns_added"] == []
    assert result["columns_removed"] == []

def test_display_data_version_diff(capsys):
    """
    Test that the display function runs without error and prints something.
    """
    df_old = pd.DataFrame({"a": [1, None]})
    df_new = pd.DataFrame({"a": [2, None]})
    result = data_version_diff(df_old, df_new)
    
    # Call the display function
    from csvplus.data_version_diff import display_data_version_diff
    display_data_version_diff(result)
    
    captured = capsys.readouterr()
    assert "DATA VERSION CHANGE SUMMARY" in captured.out
