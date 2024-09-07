import pytest
from unittest.mock import patch
from pathlib import Path
from albylib.io import get_human_readable_size, print_file_size


def test_get_human_readable_size():
    assert get_human_readable_size(500) == "500.00 B"
    assert get_human_readable_size(1024) == "1.00 KB"
    assert get_human_readable_size(1048576) == "1.00 MB"
    assert get_human_readable_size(1073741824) == "1.00 GB"
    assert get_human_readable_size(1099511627776) == "1.00 TB"


@pytest.mark.parametrize(
    "size, expected",
    [
        (1500, "1.46 KB"),
        (2000000, "1.91 MB"),
        (3000000000, "2.79 GB"),
    ],
)
def test_get_human_readable_size_parametrized(size, expected):
    assert get_human_readable_size(size) == expected


@patch('os.path.getsize')
@patch('builtins.print')
def test_print_file_size(mock_print, mock_getsize):
    mock_getsize.return_value = 1048576  # 1 MB
    file_path = Path("dummy_file.txt")

    print_file_size(file_path)

    mock_getsize.assert_called_once_with(file_path)
    mock_print.assert_called_once_with("File size: 1.00 MB")


@pytest.mark.parametrize(
    "file_path",
    [
        "dummy_file.txt",
        Path("dummy_file.txt"),
    ],
)
@patch('os.path.getsize')
@patch('builtins.print')
def test_print_file_size_path_types(mock_print, mock_getsize, file_path):
    mock_getsize.return_value = 2048  # 2 KB

    print_file_size(file_path)

    mock_getsize.assert_called_once_with(file_path)
    mock_print.assert_called_once_with("File size: 2.00 KB")
