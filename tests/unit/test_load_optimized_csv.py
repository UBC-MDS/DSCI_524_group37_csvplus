import pandas as pd
import numpy as np
import pytest
from csvplus.load_optimized_csv import load_optimized_csv


@pytest.fixture
def sample_csv(tmp_path):
    """Creates a sample CSV file for testing."""
    df = pd.DataFrame({
        "int8_col": [1, 2, 100, -100, 5],
        "int16_col": [1000, -1000, 30000, -30000, 500],
        "int32_col": [100000, -100000, 2000000, -2000000, 50000],
        "float32_col": [1.123456, 2.234567, 3.345678, 4.456789, 5.567890],
        "sparse_col": [0, 0, 0, 0, 1],
        "cat_col": ["A", "A", "B", "B", "C"],
        "normal_col": ["X", "Y", "Z", "W", "V"]
    })
    csv_file = tmp_path / "sample.csv"
    df.to_csv(csv_file, index=False)
    return str(csv_file)


def test_load_optimized_csv_basic(sample_csv):
    """Test that the function loads a CSV and returns a DataFrame."""
    df = load_optimized_csv(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    expected_cols = [
        "int8_col", "int16_col", "int32_col",
        "float32_col", "sparse_col",
        "cat_col", "normal_col"
    ]
    assert list(df.columns) == expected_cols


def test_load_optimized_csv_nrows(sample_csv):
    """Test the nrows parameter."""
    df = load_optimized_csv(sample_csv, nrows=2)
    assert len(df) == 2


def test_load_optimized_csv_usecols(sample_csv):
    """Test the usecols parameter."""
    df = load_optimized_csv(sample_csv, usecols=["int8_col", "sparse_col"])
    assert list(df.columns) == ["int8_col", "sparse_col"]


def test_load_optimized_csv_dtypes(sample_csv):
    """
    Test that the function correctly downcasts numerical columns.
    Note: This test assumes the implementation will perform the downcasting
    as described in the docstring.
    """
    df = load_optimized_csv(sample_csv)

    # Check integer downcasting
    assert df["int8_col"].dtype == "int8"
    assert df["int16_col"].dtype == "int16"
    assert df["int32_col"].dtype == "int32"

    # Check float downcasting (float32 is minimum for pandas downcast)
    assert df["float32_col"].dtype == "float32"

    # Check categorical conversion (low cardinality)
    assert isinstance(df["cat_col"].dtype, pd.CategoricalDtype)

    # Check that high cardinality columns are NOT converted to categorical
    # normal_col has 100% unique values (5 unique / 5 total)
    assert not isinstance(df["normal_col"].dtype, pd.CategoricalDtype)

    # Check sparse conversion (80% zeros)
    assert isinstance(df["sparse_col"].dtype, pd.SparseDtype)


def test_load_optimized_csv_invalid_file():
    """Test that FileNotFoundError is raised for non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_optimized_csv("non_existent_file.csv")


def test_load_optimized_csv_invalid_thresholds(sample_csv):
    """Test that ValueError is raised for invalid thresholds."""
    with pytest.raises(ValueError):
        load_optimized_csv(sample_csv, sparse_threshold=1.5)
    with pytest.raises(ValueError):
        load_optimized_csv(sample_csv, category_threshold=-0.1)


def test_load_optimized_csv_empty_file(tmp_path):
    """Test that EmptyDataError is raised for empty file."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises(pd.errors.EmptyDataError):
        load_optimized_csv(str(empty_file))


def test_load_optimized_csv_range_index(sample_csv):
    """Test that the returned DataFrame has a RangeIndex."""
    df = load_optimized_csv(sample_csv)
    assert isinstance(df.index, pd.RangeIndex)


def test_no_sparse_cols_excludes_column(sample_csv):
    """Test that no_sparse_cols excludes columns from sparse conversion."""
    df = load_optimized_csv(sample_csv, no_sparse_cols=["sparse_col"])
    assert not isinstance(df["sparse_col"].dtype, pd.SparseDtype)


def test_no_downcast_cols_excludes_column(sample_csv):
    """Test that no_downcast_cols excludes columns from downcasting."""
    df = load_optimized_csv(sample_csv, no_downcast_cols=["int8_col"])
    # Should remain int64 (default pandas int type), not downcast to int8
    assert df["int8_col"].dtype != "int8"


def test_no_category_cols_excludes_column(sample_csv):
    """Test that no_category_cols excludes columns
    from categorical conversion."""
    df = load_optimized_csv(sample_csv, no_category_cols=["cat_col"])
    assert not isinstance(df["cat_col"].dtype, pd.CategoricalDtype)


def test_kwargs_passthrough(tmp_path):
    """Test that kwargs are passed through to pandas.read_csv."""
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    csv_file = tmp_path / "semicolon.csv"
    df.to_csv(csv_file, index=False, sep=";")
    result = load_optimized_csv(str(csv_file), sep=";")
    assert list(result.columns) == ["a", "b"]
    assert len(result) == 2


def test_invalid_type_raises_typeerror(sample_csv):
    """Test that TypeError is raised for invalid argument types."""
    with pytest.raises(TypeError):
        load_optimized_csv(sample_csv, nrows="not_an_int")
    with pytest.raises(TypeError):
        load_optimized_csv(sample_csv, usecols="not_a_list")
    with pytest.raises(TypeError):
        load_optimized_csv(123)  # filepath should be str


def test_sparse_threshold_controls_conversion(tmp_path):
    """Test that sparse_threshold affects which columns become sparse."""
    # 60% zeros - should be sparse at 0.3 threshold, not at 0.7
    df = pd.DataFrame({"col": [0, 0, 0, 0, 0, 0, 1, 2, 3, 4]})
    csv_file = tmp_path / "sparse_test.csv"
    df.to_csv(csv_file, index=False)

    df_sparse = load_optimized_csv(str(csv_file), sparse_threshold=0.3)
    assert isinstance(df_sparse["col"].dtype, pd.SparseDtype)

    df_not_sparse = load_optimized_csv(str(csv_file), sparse_threshold=0.7)
    assert not isinstance(df_not_sparse["col"].dtype, pd.SparseDtype)


def test_category_threshold_controls_conversion(tmp_path):
    """Test that category_threshold affects
    which columns become categorical."""
    # 20% unique (2 unique / 10 total)
    df = pd.DataFrame({"col": ["A", "A", "A", "A", "A",
                               "B", "B", "B", "B", "B"]})
    csv_file = tmp_path / "cat_test.csv"
    df.to_csv(csv_file, index=False)

    df_cat = load_optimized_csv(str(csv_file), category_threshold=0.3)
    assert isinstance(df_cat["col"].dtype, pd.CategoricalDtype)

    df_not_cat = load_optimized_csv(str(csv_file), category_threshold=0.1)
    assert not isinstance(df_not_cat["col"].dtype, pd.CategoricalDtype)


def test_threshold_boundary_values(sample_csv):
    """Test that threshold boundary values (0 and 1) are accepted."""
    # These should not raise errors
    df = load_optimized_csv(sample_csv, sparse_threshold=0.0)
    assert isinstance(df, pd.DataFrame)

    df = load_optimized_csv(sample_csv, sparse_threshold=1.0)
    assert isinstance(df, pd.DataFrame)

    df = load_optimized_csv(sample_csv, category_threshold=0.0)
    assert isinstance(df, pd.DataFrame)

    df = load_optimized_csv(sample_csv, category_threshold=1.0)
    assert isinstance(df, pd.DataFrame)


def test_data_integrity_preserved(sample_csv):
    """Test that data values are preserved after optimization
    (same rows, columns, values)."""
    # Load the original data without optimization
    df_original = pd.read_csv(sample_csv)

    # Load with optimization
    df_optimized = load_optimized_csv(sample_csv)

    # Check same shape
    assert df_original.shape == df_optimized.shape, \
        "Shape mismatch after optimization"

    # Check same columns
    assert list(df_original.columns) == list(df_optimized.columns), \
        "Columns mismatch after optimization"

    # Check same values
    # (compare after converting to common types for comparison)
    for col in df_original.columns:
        # Convert both to numpy arrays for comparison
        # (handles sparse and categorical)
        original_values = df_original[col].to_numpy()
        optimized_values = np.array(df_optimized[col])

        if pd.api.types.is_numeric_dtype(df_original[col]):
            # For numeric columns, use np.allclose to handle floating point
            assert np.allclose(original_values,
                               optimized_values, equal_nan=True), \
                f"Values mismatch in column '{col}'"
        else:
            # For non-numeric, compare directly
            assert np.array_equal(original_values, optimized_values), \
                f"Values mismatch in column '{col}'"


def test_file_with_headers_only(tmp_path):
    """Test that EmptyDataError is raised for
    file with headers but no data rows."""
    csv_file = tmp_path / "headers_only.csv"
    csv_file.write_text("col1,col2,col3\n")
    with pytest.raises(pd.errors.EmptyDataError):
        load_optimized_csv(str(csv_file))


def test_usecols_invalid_column(tmp_path):
    """Test that ValueError is raised for usecols with non-existent column."""
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    csv_file = tmp_path / "usecols_test.csv"
    df.to_csv(csv_file, index=False)
    with pytest.raises(ValueError):
        load_optimized_csv(str(csv_file), usecols=["nonexistent_col"])


def test_boolean_column_preserved(tmp_path):
    """Test that boolean columns are preserved and not converted to sparse."""
    df = pd.DataFrame({
        "bool_col": [True, False, False, False, False],  # 80% False
        "int_col": [0, 0, 0, 0, 1]  # 80% zeros
    })
    csv_file = tmp_path / "bool_test.csv"
    df.to_csv(csv_file, index=False)

    result = load_optimized_csv(str(csv_file), sparse_threshold=0.3)

    # Boolean column should remain bool, not converted to sparse
    assert result["bool_col"].dtype == "bool"
    assert not isinstance(result["bool_col"].dtype, pd.SparseDtype)

    # Integer column should be converted to sparse (80% zeros > 30% threshold)
    assert isinstance(result["int_col"].dtype, pd.SparseDtype)


def test_mixed_type_column_handling(tmp_path):
    """Test that mixed-type object columns
    don't crash and are handled gracefully."""
    csv_file = tmp_path / "mixed.csv"
    csv_file.write_text("col\n1\nfoo\n2.5\nbar\n")

    df = load_optimized_csv(str(csv_file))

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4
    # Mixed types become object, may be converted to categorical
    assert df["col"].dtype == "object" or isinstance(df["col"].dtype,
                                                     pd.CategoricalDtype)


def test_nan_values_preserved(tmp_path):
    """Test that NaN values are preserved after optimization."""
    df = pd.DataFrame({
        "num_col": [0.0, 0.0, np.nan, np.nan, 1.0],
        "str_col": ["A", "A", None, "B", "B"]
    })
    csv_file = tmp_path / "nan_test.csv"
    df.to_csv(csv_file, index=False)

    result = load_optimized_csv(str(csv_file))

    # NaN values should be preserved
    assert result["num_col"].isna().sum() == 2
    assert result["str_col"].isna().sum() == 1
