"""
Load a CSV file and return a memory-optimized DataFrame.
"""
import pandas as pd


def load_optimized_csv(
    filepath: str,
    nrows: int | None = None,
    usecols: list[str] | None = None,
    no_sparse_cols: list[str] | None = None,
    no_downcast_cols: list[str] | None = None,
    no_category_cols: list[str] | None = None,
    sparse_threshold: float = 0.3,
    category_threshold: float = 0.7,
    **kwargs
) -> pd.DataFrame:
    """
    Load a CSV as a memory-optimized DataFrame with type downcasting
    and categorical/sparse conversions.

    Automatically determines optimal chunk size based on file size and
    available system memory, then processes each chunk by downcasting
    dtypes, converting low-cardinality string columns to categorical,
    and converting high-zero-density columns to sparse. Returns a single
    concatenated, memory-optimized DataFrame with a RangeIndex.

    Parameters
    ----------
    filepath : str
        Path to the CSV file to load.
    nrows : int, optional
        Maximum number of rows to read. If None, reads all rows.
    usecols : list of str, optional
        Columns to read. If None, reads all columns.
    no_sparse_cols : list of str, optional
        Columns to exclude from sparse conversion.
    no_downcast_cols : list of str, optional
        Columns to exclude from dtype downcasting.
    no_category_cols : list of str, optional
        Columns to exclude from categorical conversion.
    sparse_threshold : float, default 0.3
        Minimum proportion of zeros required to convert a column to sparse.
        Must be between 0 and 1.
    category_threshold : float, default 0.7
        Maximum ratio of unique values to total values for a string column
        to be converted to categorical. Must be between 0 and 1.
    **kwargs
        Additional keyword arguments passed to `pandas.read_csv`
        (e.g., `sep`, `encoding`, `parse_dates`).

    Returns
    -------
    pd.DataFrame
        A memory-optimized DataFrame with:
        - Numeric columns downcasted to smallest sufficient dtype
        - Low-cardinality string columns converted to categorical
        - High-zero columns converted to SparseDtype
        - RangeIndex set as index

    Raises
    ------
    FileNotFoundError
        If `filepath` does not exist.
    ValueError
        If the file is not a valid CSV, if `sparse_threshold` or
        `category_threshold` are not in [0, 1], or if `usecols`
        contains columns not present in the CSV.
    TypeError
        If arguments are of incorrect types.
    pd.errors.EmptyDataError
        If the CSV file is empty or contains only headers.
    MemoryError
        If the final DataFrame exceeds available memory.

    Examples
    --------
    >>> df = load_optimized_csv(
    ...     "large_dataset.csv",
    ...     nrows=100000,
    ...     usecols=["id", "value", "category", "status"],
    ...     no_sparse_cols=["id"],
    ...     no_downcast_cols=["value"],
    ...     no_category_cols=["id"],
    ...     sparse_threshold=0.6,
    ...     category_threshold=0.3,
    ... )
    >>> df.info(memory_usage="deep")
    """
    # Type validation
    if not isinstance(filepath, str):
        raise TypeError("filepath must be a string")
    if nrows is not None and not isinstance(nrows, int):
        raise TypeError("nrows must be an integer or None")
    if usecols is not None and not isinstance(usecols, list):
        raise TypeError("usecols must be a list or None")
    if no_sparse_cols is not None and not isinstance(no_sparse_cols, list):
        raise TypeError("no_sparse_cols must be a list or None")
    if no_downcast_cols is not None and not isinstance(no_downcast_cols, list):
        raise TypeError("no_downcast_cols must be a list or None")
    if no_category_cols is not None and not isinstance(no_category_cols, list):
        raise TypeError("no_category_cols must be a list or None")

    # Threshold validation
    if not (0 <= sparse_threshold <= 1):
        raise ValueError("sparse_threshold must be between 0 and 1")
    if not (0 <= category_threshold <= 1):
        raise ValueError("category_threshold must be between 0 and 1")

    # File existence check
    import os
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Initialize exclusion lists
    no_sparse_cols = no_sparse_cols or []
    no_downcast_cols = no_downcast_cols or []
    no_category_cols = no_category_cols or []

    # Determine optimal chunk size based on file size and available memory
    file_size = os.path.getsize(filepath)
    try:
        import psutil
        available_memory = psutil.virtual_memory().available
    except ImportError:
        # Default to 1GB if psutil not available
        available_memory = 1024 * 1024 * 1024

    # Use ~10% of available memory per chunk, minimum 10KB, maximum 100MB
    target_chunk_bytes = max(10 * 1024,
                             min(available_memory // 10, 100 * 1024 * 1024))

    # Estimate rows per chunk (rough estimate: assume avg 100 bytes per row)
    estimated_bytes_per_row = (max(100, file_size // 10000)
                               if file_size > 0 else 100)
    chunksize = max(1000, target_chunk_bytes // estimated_bytes_per_row)

    # Helper function to optimize a chunk
    def _optimize_chunk(chunk_df):
        # Downcast numeric columns (skip booleans)
        for col in chunk_df.columns:
            if col in no_downcast_cols:
                continue
            if pd.api.types.is_bool_dtype(chunk_df[col]):
                continue  # Preserve boolean dtype
            if pd.api.types.is_integer_dtype(chunk_df[col]):
                chunk_df[col] = pd.to_numeric(chunk_df[col],
                                              downcast="integer")
            elif pd.api.types.is_float_dtype(chunk_df[col]):
                chunk_df[col] = pd.to_numeric(chunk_df[col],
                                              downcast="float")
        return chunk_df

    # Read CSV in chunks
    chunks = []
    rows_read = 0

    for chunk in pd.read_csv(filepath, usecols=usecols,
                             chunksize=chunksize, **kwargs):
        # Apply nrows limit
        if nrows is not None:
            remaining = nrows - rows_read
            if remaining <= 0:
                break
            if len(chunk) > remaining:
                chunk = chunk.iloc[:remaining]

        # Optimize the chunk (downcast numerics)
        chunk = _optimize_chunk(chunk)
        chunks.append(chunk)
        rows_read += len(chunk)

        if nrows is not None and rows_read >= nrows:
            break

    # Handle empty file or no chunks read
    if not chunks:
        raise pd.errors.EmptyDataError("No columns to parse from file")

    # Concatenate all chunks
    df = pd.concat(chunks, ignore_index=True)

    # Handle headers-only file (no data rows)
    if len(df) == 0:
        raise pd.errors.EmptyDataError(("CSV file contains only headers, "
                                       "no data rows"))

    # Convert low-cardinality string columns to categorical
    # (after concat for accurate ratios)
    for col in df.columns:
        if col in no_category_cols:
            continue
        if pd.api.types.is_object_dtype(df[col]):
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio <= category_threshold:
                df[col] = df[col].astype("category")

    # Convert high-zero columns to sparse (after concat for accurate ratios)
    # Skip boolean columns to preserve their dtype
    for col in df.columns:
        if col in no_sparse_cols:
            continue
        if pd.api.types.is_bool_dtype(df[col]):
            continue  # Preserve boolean dtype
        if (pd.api.types.is_numeric_dtype(df[col]) and
                not isinstance(df[col].dtype, pd.SparseDtype)):
            zero_ratio = (df[col] == 0).sum() / len(df)
            if zero_ratio >= sparse_threshold:
                df[col] = df[col].astype(pd.SparseDtype(df[col].dtype,
                                                        fill_value=0))

    # Ensure RangeIndex
    df = df.reset_index(drop=True)

    return df
