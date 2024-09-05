from pandas import DataFrame


def check_column_match(df1: DataFrame, primary_key_column: str, df2: DataFrame, foreign_key_column: str) -> bool:
    """
    Check if all values in column2 of df2 are present in column1 of df1.

    Parameters:
    df1 (DataFrame): The first DataFrame to check.
    column1 (str): The column in the first DataFrame to check for matches.
    df2 (DataFrame): The second DataFrame to check.
    column2 (str): The column in the second DataFrame to check for matches.

    Returns:
    bool: True if all values in column2 of df2 are present in column1 of df1, 
    False otherwise.

    Raises:
    ValueError: If either column does not exist in its respective DataFrame.
    """
    if primary_key_column not in df1.columns:
        raise ValueError(
            f'Error: The column "{primary_key_column}" does not exist in the first DataFrame.')
    if foreign_key_column not in df2.columns:
        raise ValueError(
            f'Error: The column "{foreign_key_column}" does not exist in the second DataFrame.')
    return df2[foreign_key_column].isin(df1[primary_key_column]).all()
