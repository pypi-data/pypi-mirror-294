import pandas as pd


def move_columns(df: pd.DataFrame, cols_to_move: list, new_index: int) -> pd.DataFrame:
    """
    This method re-arranges the columns in a dataframe to place the desired columns at the desired index.
    ex Usage: df = move_columns(df, ['Rev'], 2)

    Args:
        df: A input DataFrame
        cols_to_move: The names of the columns to move. They must be a list
        new_index: The 0-based location to place the columns.
    Returns:
        a dataframe with the columns re-arranged
    """
    other = [c for c in df if c not in cols_to_move]
    if new_index > (len(df.columns) - 1) or new_index < 0:
        raise IndexError("Index is out of range")
    start = other[0:new_index]
    end = other[new_index:]
    return df[start + cols_to_move + end]
