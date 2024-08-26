import pytest
from pro_filer.actions.main_actions import find_duplicate_files


def test_no_duplicate_files(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Content of file 1")

    file2 = tmp_path / "file2.txt"
    file2.write_text("Content of file 2")

    context = {"all_files": [str(file1), str(file2)]}

    result = find_duplicate_files(context)

    assert result == []


def test_duplicate_files_found(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Duplicated content")

    file2 = tmp_path / "file2.txt"
    file2.write_text("Duplicated content")

    file3 = tmp_path / "file3.txt"
    file3.write_text("Duplicated content")

    context = {"all_files": [str(file1), str(file2), str(file3)]}

    result = find_duplicate_files(context)

    expected = [
        (str(file1), str(file2)),
        (str(file1), str(file3)),
        (str(file2), str(file3)),
    ]

    assert result == expected


def test_non_existent_file_raises_value_error(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Content of file 1")

    non_existent_file = tmp_path / "non_existent.txt"

    context = {"all_files": [str(file1), str(non_existent_file)]}

    with pytest.raises(ValueError, match="All files must exist"):
        find_duplicate_files(context)


def test_files_with_same_name_but_different_content(tmp_path):
    file1 = tmp_path / "dir1" / "file.txt"
    file1.parent.mkdir()
    file1.write_text("Content of file 1")

    file2 = tmp_path / "dir2" / "file.txt"
    file2.parent.mkdir()
    file2.write_text("Conmtent of file 2")

    context = {"all_files": [str(file1), str(file2)]}

    result = find_duplicate_files(context)

    assert result == []
