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
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024


def print_file_size(file_path: Union[str, Path]):
    file_size = os.path.getsize(file_path)
    print(f"File size: {get_human_readable_size(file_size)}")
