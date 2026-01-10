import pandas as pd

def load_optimized_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """
    Loads a CSV file and automatically downcasts data types to minimize memory footprint.

    Args:
        filepath (str): Path to the CSV file to load.
        **kwargs: Arbitrary keyword arguments passed directly to `pandas.read_csv` and potentially other args
            (e.g., `sep`, `index_col`, `usecols`).

    Returns:
        pd.DataFrame: A memory-optimized DataFrame.

    Raises:
        MemoryError: If the file size significantly exceeds available system memory.
        FileNotFoundError: If the filepath does not exist.

    Example:
        >>> df = load_optimized_csv(
        ...     "large_dataset.csv"
        ... )
        >>> print(df.dtypes)
    """
    # TODO: implement this function
    pass