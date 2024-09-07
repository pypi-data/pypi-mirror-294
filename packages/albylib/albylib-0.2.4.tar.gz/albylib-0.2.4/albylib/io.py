from pathlib import Path
from typing import Union
import os

import pandas as pd


def read_glob(path: Union[str, Path], glob_pattern: str):
    ds = []
    for i in Path(path).glob(glob_pattern):
        d = pd.read_table(i)
        ds.append(d)
    return pd.concat(ds).reset_index(drop=True)


def get_human_readable_size(size_in_bytes):
    """
    Convert a size in bytes to a human-readable string representation.

    Args:
        size_in_bytes (int): The size in bytes to convert.

    Returns:
        str: A human-readable string representation of the size, including the appropriate unit.

    This function takes a size in bytes and converts it to a human-readable format,
    using the appropriate unit (B, KB, MB, GB, TB, or PB). The result is rounded
    to two decimal places.
    """
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024


def print_file_size(file_path: Union[str, Path]):
    """
    Print the size of a file in a human-readable format.

    Args:
        file_path (Union[str, Path]): The path to the file. Can be a string or a Path object.

    Returns:
        None

    This function calculates the size of the specified file and prints it in a human-readable format
    (e.g., B, KB, MB, GB, TB, PB) using the get_human_readable_size function.
    """
    file_size = os.path.getsize(file_path)
    print(f"File path: {file_path}")
    print(f"File size: {get_human_readable_size(file_size)}")
