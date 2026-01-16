import pandas as pd
import numpy as np
import pytest
from rapidfuzz import process, fuzz
from csvplus.data_correction import resolve_string_value

@pytest.fixture
def company_data():
    data = pd.DataFrame({
         "company_name": ["Google", "Google Inc.", "Gogle", "Microsoftt", "Micro-soft"],
         "location": ["Mt. view", "Mt. view", "Mt. view", "Redmond", "Redmond"]
    })
    return data

def test_column_name_error(data):
    """Test that includes a nonexistent column name."""
    with pytest.raises(ValueError, match="The given column_name does not exist."):
        resolve_string_value(data, "store_name", ["Google", "Microsoft"], 80)

def test_resolved_names_error(data):
    """Test that has an empty resolved_names list."""
    with pytest.raises(ValueError, match="The given resolved names is empty."):
        resolve_string_value(data, "company_name", [], 80)

def test_threshold_value_error(data):
    """Test that includes an out-of-range threshold value."""
    with pytest.raises(ValueError, match="The threshold value is out of range."):
        resolve_string_value(data, "company_name", ["Google", "Microsoft"], -1)

@pytest.mark.parametrize(
    "threshold_value, expected_list",
    [
        (90, ["Google", "Microsoft"]),
        (94, ["Google", "Google Inc.", "Gogle", "Microsoft"])
    ]
)
def test_resolve_string_value(data, threshold_value, expected_list):
    """Test that includes an out-of-range threshold value."""
    column_name = "company_name"
    resolve_string_value(data, column_name, ["Google", "Microsoft"], threshold_value)
    # Test if the entire thing is expected.
    assert set(data[column_name].unique()) == set(expected_list)