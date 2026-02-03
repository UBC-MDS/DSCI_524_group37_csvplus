"""
LLM Usage Disclosure
Claude.ai was used to perform the following tasks:
- After writing initial tests, suggest additional tests for maximum coverage.
- Suggest edge cases that should be addressed in test suite and function code.
- Troubleshooting test construction, particularly dealing with testing for
  Null and NaN values.
"""

import pytest
import pandas as pd
import numpy as np
from csvplus.generate_report import summary_report


def test_non_dataframe_input_raises_typeerror():
    """Test that a non-DataFrame input raises a TypeError."""
    with pytest.raises(TypeError):
        summary_report([1, 2, 3])


def test_empty_dataframe_raises_valueerror():
    """Test that an empty DataFrame input raises a ValueError."""
    df = pd.DataFrame()
    with pytest.raises(ValueError):
        summary_report(df)


def test_confidence_level_negative_raises_valueerror():
    """Test that a negative confidence_level raises ValueError."""
    df = pd.DataFrame({'x': [1, 2, 3]})
    with pytest.raises(ValueError):
        summary_report(df, confidence_level=-0.1)


def test_confidence_level_above_one_raises_valueerror():
    """Test that a confidence_level greater than one raises ValueError."""
    df = pd.DataFrame({'x': [1, 2, 3]})
    with pytest.raises(ValueError):
        summary_report(df, confidence_level=1.1)


def test_top_n_zero_raises_valueerror():
    """Test that a top_n with value 0 raises ValueError."""
    df = pd.DataFrame({'x': ['a', 'b', 'c']})
    with pytest.raises(ValueError):
        summary_report(df, top_n=0)


def test_top_n_negative_raises_valueerror():
    """Test that a negative top_n raises ValueError"""
    df = pd.DataFrame({'x': ['a', 'b', 'c']})
    with pytest.raises(ValueError):
        summary_report(df, top_n=-1)


def test_top_n_greater_than_unique():
    """Test that top_n larger than the number of unique values,
    returns all unique values without error."""
    df = pd.DataFrame({'x': ['a', 'b', 'c', 'c']})
    _, cat_stats = summary_report(df, top_n=100)

    top_vals = cat_stats.loc['x', 'top_values']
    assert len(top_vals) == 3
    assert set(top_vals.keys()) == {'a', 'b', 'c'}


def test_numeric_basic():
    """Test creation of numeric report with basic inputs."""
    df = pd.DataFrame({'age': [25, 21, 32, 40]})
    num_stats, _ = summary_report(df)

    assert num_stats.loc['age', 'count'] == 4
    assert num_stats.loc['age', 'n_missing'] == 0
    assert num_stats.loc['age', 'missing_prop'] == 0.0
    assert num_stats.loc['age', 'mean'] == 29.5
    assert num_stats.loc['age', 'median'] == 28.5
    assert num_stats.loc['age', 'min'] == 21
    assert num_stats.loc['age', 'max'] == 40
    assert num_stats.loc['age', 'n_unique'] == 4


def test_numeric_missing_values():
    """Test creation of numeric report where
    input DataFrame contains missing values."""
    df = pd.DataFrame({'x': [10, None, 20, None, 30]})
    num_stats, _ = summary_report(df)

    assert num_stats.loc['x', 'count'] == 3
    assert num_stats.loc['x', 'n_missing'] == 2
    assert num_stats.loc['x', 'missing_prop'] == 0.4
    assert num_stats.loc['x', 'mean'] == 20.0


def test_ci_calculation():
    """Test the calculation of a confidence interval."""
    df = pd.DataFrame({'x': [10, 20, 30, 40, 50]})
    num_stats, _ = summary_report(df, confidence_level=0.95)

    assert 'ci_lower' in num_stats.columns
    assert 'ci_upper' in num_stats.columns
    assert num_stats.loc['x', 'ci_lower'] < num_stats.loc['x', 'mean']
    assert num_stats.loc['x', 'ci_upper'] > num_stats.loc['x', 'mean']


def test_ci_single_value():
    """Test that a confidence interval is not created
    when DataFrame contains only a single numeric value."""
    df = pd.DataFrame({'x': [42]})
    num_stats, _ = summary_report(df)

    assert num_stats.loc['x', 'count'] == 1
    assert pd.isna(num_stats.loc['x', 'ci_lower'])
    assert pd.isna(num_stats.loc['x', 'ci_upper'])


def test_different_confidence_levels():
    """Test that different confidence levels return
    the correct widths for their respective CIs."""
    df = pd.DataFrame({'x': list(range(100))})
    ci_95, _ = summary_report(df, confidence_level=0.95)
    ci_99, _ = summary_report(df, confidence_level=0.99)

    # Verify that 99% CI is wider than 95% CI
    ci_95_width = ci_95.loc['x', 'ci_upper'] - ci_95.loc['x', 'ci_lower']
    ci_99_width = ci_99.loc['x', 'ci_upper'] - ci_99.loc['x', 'ci_lower']
    assert ci_99_width > ci_95_width


def test_integer_and_float_dtypes():
    """Test that both integers and floats are processed correctly."""
    df = pd.DataFrame({
        'int_col': [1, 2, 3],
        'float_col': [1.1, 2.2, 3.3]
    })
    num_stats, _ = summary_report(df)

    assert 'int_col' in num_stats.index
    assert 'float_col' in num_stats.index


def test_quartile_calculations():
    """Test that the quartile calculations are correct."""
    df = pd.DataFrame({'vals': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
    num_stats, _ = summary_report(df)

    assert num_stats.loc['vals', '25%'] == 3.25
    assert num_stats.loc['vals', 'median'] == 5.5
    assert num_stats.loc['vals', '75%'] == 7.75


def test_categorical_basic():
    """Test creation of categorical report with basic inputs."""
    df = pd.DataFrame({'city': ['NYC', 'LA', 'NYC', 'SF', 'LA']})
    _, cat_stats = summary_report(df)

    assert cat_stats.loc['city', 'count'] == 5
    assert cat_stats.loc['city', 'n_missing'] == 0
    assert cat_stats.loc['city', 'n_unique'] == 3
    assert cat_stats.loc['city', 'unique_prop'] == 0.6
    assert cat_stats.loc['city', 'is_constant'] == np.False_


def test_categorical_with_missing():
    """Test creation of categorical report where
    input DataFrame contains missing values."""
    df = pd.DataFrame({'cat': ['a', None, 'b', None, 'a']})
    _, cat_stats = summary_report(df)

    assert cat_stats.loc['cat', 'count'] == 3
    assert cat_stats.loc['cat', 'n_missing'] == 2
    assert cat_stats.loc['cat', 'missing_prop'] == 0.4


def test_is_constant():
    """Test that 'is_constant' is True when a column
    contains all identical values."""
    df = pd.DataFrame({'const': ['same', 'same', 'same']})
    _, cat_stats = summary_report(df)

    assert cat_stats.loc['const', 'is_constant'] is np.True_
    assert cat_stats.loc['const', 'n_unique'] == 1


def test_top_values_default_n():
    """Test that 'top_values' returns the correct value
    with default parameters."""
    df = pd.DataFrame({'x': ['a']*10 + ['b']*5 +
                       ['c']*3 + ['d']*2 + ['e']*1})
    _, cat_stats = summary_report(df)

    top_vals = cat_stats.loc['x', 'top_values']
    assert len(top_vals) == 5
    assert top_vals['a'] == 10
    assert top_vals['b'] == 5


def test_top_values_custom_n():
    """Test that 'top_values' returns the correct value
    with custom parameters."""
    df = pd.DataFrame({'x': ['a']*10 + ['b']*5 + ['c']*3 + ['d']*2})
    _, cat_stats = summary_report(df, top_n=2)

    top_vals = cat_stats.loc['x', 'top_values']
    assert len(top_vals) == 2
    assert 'a' in top_vals
    assert 'b' in top_vals
    assert 'c' not in top_vals
    assert 'd' not in top_vals


def test_top_1_prop():
    """Test that 'top_1_prop' returns the correct value."""
    df = pd.DataFrame({'cat': ['a', 'a', 'a', 'b', 'c']})
    _, cat_stats = summary_report(df)

    assert cat_stats.loc['cat', 'top_1_prop'] == 0.6


def test_boolean_is_categorical():
    """Test that boolean objects are correctly
    treated as categorical."""
    df = pd.DataFrame({'flag': [True, False, True, True]})
    _, cat_stats = summary_report(df)

    assert 'flag' in cat_stats.index


def test_datetime_is_categorical():
    """Test that datetime objects are correctly
    treated as categorical."""
    df = pd.DataFrame({
        'date': pd.to_datetime(['2026-01-09', '2026-06-25', '2025-12-31'])
    })
    _, cat_stats = summary_report(df)

    assert 'date' in cat_stats.index


def test_string_and_object_dtypes():
    """Test that strings and objects are processed correctly."""
    df = pd.DataFrame({
        'str_col': pd.Series(['a', 'b'], dtype='string'),
        'obj_col': pd.Series(['x', 'y'], dtype='object')
    })
    _, cat_stats = summary_report(df)

    assert 'str_col' in cat_stats.index
    assert 'obj_col' in cat_stats.index


def test_category_dtype():
    """Test that the category dtype is processed correctly."""
    df = pd.DataFrame({
        'cat_col': pd.Categorical(['low', 'high', 'medium'])
    })
    _, cat_stats = summary_report(df)

    assert 'cat_col' in cat_stats.index


def test_mixed_columns():
    """Test the creation of a report using a
    DataFrame with different column types."""
    df = pd.DataFrame({
        'age': [25, 30, 35],
        'city': ['NYC', 'LA', 'SF'],
        'salary': [50000, 60000, 70000]
    })
    num_stats, cat_stats = summary_report(df)

    assert set(num_stats.index) == {'age', 'salary'}
    assert set(cat_stats.index) == {'city'}


def test_only_numeric_columns():
    """Test the creation of a report using a
    DataFrame with multiple numeric columns."""
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4.0, 5.0, 6.0]
    })
    num_stats, cat_stats = summary_report(df)

    assert len(num_stats) == 2
    assert len(cat_stats) == 0


def test_only_categorical_columns():
    """Test the creation of a report using a
    DataFrame with multiple categorical columns."""
    df = pd.DataFrame({
        'x': ['a', 'b', 'c'],
        'y': ['d', 'e', 'f']
    })
    num_stats, cat_stats = summary_report(df)

    assert len(num_stats) == 0
    assert len(cat_stats) == 2


def test_single_row_dataframe():
    """Test function using DataFrame with a single row."""
    df = pd.DataFrame({'a': [1], 'b': ['x']})
    num_stats, cat_stats = summary_report(df)

    assert num_stats.loc['a', 'count'] == 1
    assert cat_stats.loc['b', 'count'] == 1


def test_single_column_dataframe():
    """Test function using DataFrame with a single column."""
    df = pd.DataFrame({'only': [1, 2, 3]})
    num_stats, _ = summary_report(df)

    assert len(num_stats) == 1


def test_extreme_unique_values():

    df = pd.DataFrame({'id': range(10000)})
    num_stats, _ = summary_report(df)
    """Test function using DataFrame with a large number of
    unique rows."""
    assert num_stats.loc['id', 'n_unique'] == 10000


def test_all_null_columns_excluded():
    """Test that all-null columns are correctly
    excluded from both numeric and categorical stats."""
    df = pd.DataFrame({
        'numeric_col': [1, 2, 3],
        'all_null_numeric': [None, None, None],
        'cat_col': ['a', 'b', 'c'],
        'all_null_object': [None, None, None]
    })
    num_stats, cat_stats = summary_report(df)

    assert 'all_null_numeric' not in num_stats.index
    assert 'all_null_object' not in cat_stats.index
    assert 'numeric_col' in num_stats.index
    assert 'cat_col' in cat_stats.index
    assert len(num_stats) == 1
    assert len(cat_stats) == 1


def test_all_columns_all_null():
    """Test that a DataFrame with all columns as all-null
    executes gracefully."""
    df = pd.DataFrame({
        'a': [None, None],
        'b': [None, None]
    })
    num_stats, cat_stats = summary_report(df)

    assert True


def test_extreme_confidence_levels():
    """Test the creation of CIs using extreme
    confidence_level values."""
    df = pd.DataFrame({'x': range(100)})

    # Very narrow CI
    num_low, _ = summary_report(df, confidence_level=0.0001)
    # Very wide CI
    num_high, _ = summary_report(df, confidence_level=0.9999)

    assert num_low.loc['x', 'ci_upper'] - num_low.loc['x', 'ci_lower'] < \
           num_high.loc['x', 'ci_upper'] - num_high.loc['x', 'ci_lower']


def test_duplicate_values_in_categorical():
    """Test the function for a DataFrame containing
    only an identical categorical value."""
    df = pd.DataFrame({'dup': ['a'] * 100})
    _, cat_stats = summary_report(df)

    assert cat_stats.loc['dup', 'is_constant'] == np.True_
    assert cat_stats.loc['dup', 'top_1_prop'] == 1.0
