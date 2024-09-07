import pandas as pd
import pytest

from albylib.pandas import move_columns


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9], "D": [10, 11, 12]})


def test_move_columns_basic(sample_dataframe):
    df = move_columns(sample_dataframe, ["B"], 2)
    assert list(df.columns) == ["A", "C", "B", "D"]


def test_move_columns_to_start(sample_dataframe):
    df = move_columns(sample_dataframe, ["C"], 0)
    assert list(df.columns) == ["C", "A", "B", "D"]


def test_move_columns_to_end(sample_dataframe):
    df = move_columns(sample_dataframe, ["A"], 3)
    assert list(df.columns) == ["B", "C", "D", "A"]


def test_move_multiple_columns(sample_dataframe):
    df = move_columns(sample_dataframe, ["A", "B"], 2)
    assert list(df.columns) == ["C", "D", "A", "B"]


def test_move_columns_invalid_column(sample_dataframe):
    with pytest.raises(KeyError):
        move_columns(sample_dataframe, ["E"], 2)


def test_move_columns_invalid_index(sample_dataframe):
    with pytest.raises(IndexError):
        move_columns(sample_dataframe, ["A"], 5)


def test_move_columns_negative_index(sample_dataframe):
    with pytest.raises(IndexError):
        move_columns(sample_dataframe, ["A"], -2)


def test_move_columns_same_index_no_change(sample_dataframe):
    df = move_columns(sample_dataframe, ["A"], 0)
    assert list(df.columns) == ["A", "B", "C", "D"]
