import pytest
from pro_filer.actions.main_actions import show_preview


@pytest.fixture
def context():
    return {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
        ],
        "all_dirs": ["src", "src/utils"],
    }


def test_show_preview_empty(capsys):
    context = {"all_files": [], "all_dirs": []}
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == "Found 0 files and 0 directories\n"


def test_show_preview_success_output(capsys, context):
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == (
        "Found 3 files and 2 directories\n"
        "First 5 files: ['src/__init__.py', 'src/app.py', "
        "'src/utils/__init__.py']\n"
        "First 5 directories: ['src', 'src/utils']\n"
    )


def test_show_preview_more_than_five_files(capsys):
    context = {
        "all_files": [
            "src/__init__.py",
            "src/app.py",
            "src/utils/__init__.py",
            "src/utils/file1.py",
            "src/utils/file2.py",
            "src/utils/file3.py",
        ],
        "all_dirs": ["src", "src/utils"],
    }
    show_preview(context)
    captured = capsys.readouterr()
    assert captured.out == (
        "Found 6 files and 2 directories\n"
        "First 5 files: ['src/__init__.py', 'src/app.py', "
        "'src/utils/__init__.py', 'src/utils/file1.py', "
        "'src/utils/file2.py']\n"
        "First 5 directories: ['src', 'src/utils']\n"
    )
