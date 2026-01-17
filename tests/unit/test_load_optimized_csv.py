import pandas as pd
import numpy as np
import pytest
import os
from csvplus.load_optimized_csv import load_optimized_csv

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a sample CSV file for testing."""
    df = pd.DataFrame({
        "int8_col": [1, 2, 100, -100, 5],
        "int16_col": [1000, -1000, 30000, -30000, 500],
        "int32_col": [100000, -100000, 2000000, -2000000, 50000],
        "float16_col": [1.0, 2.5, 10.1, -5.5, 0.0],
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
        "float16_col", "float32_col", "sparse_col", 
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
    
    # Check float downcasting
    assert df["float16_col"].dtype == "float16"
    assert df["float32_col"].dtype == "float32"
    
    # Check categorical conversion
    assert isinstance(df["cat_col"].dtype, pd.CategoricalDtype)
    
    # Check sparse conversion
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
