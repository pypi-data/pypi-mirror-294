from pandas import DataFrame


def assert_that_there_are_not_nulls(df: DataFrame, field_name: str) -> bool:
    """
    Checks for null values in a specified column of a DataFrame.

    Parameters:
    df : The DataFrame to check.
    field_name : The name of the column to check for null values.

    Returns:
    bool: True if there are null values in the column, False if there are no null values.

    Raises:
    TypeError: If the field_name is not a string.
    ValueError: If the field_name is not a column in the DataFrame.
    """
    if not isinstance(field_name, str):
        raise TypeError('Error: Field name must be a string.')

    if field_name not in df.columns:
        raise ValueError(f'Error: Field "{field_name}" not in DataFrame.')

    return df[field_name].isnull().any()
