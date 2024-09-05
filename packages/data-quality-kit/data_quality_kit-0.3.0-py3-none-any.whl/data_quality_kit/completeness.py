from pandas import DataFrame


def assert_that_dataframe_is_empty(df: DataFrame) -> bool:
    """
    Check if a DataFrame is empty.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to check for emptiness.

    Returns
    -------
    bool
        True if the DataFrame is empty, False otherwise.
    """
    return df.empty
