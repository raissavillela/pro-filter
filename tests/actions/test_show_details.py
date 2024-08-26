import pytest
from pro_filer.actions.main_actions import show_details
from datetime import date


@pytest.fixture
def context():
    return {"base_path": "test_file.txt"}


@pytest.fixture
def bad_context():
    return {"base_path": "test_file.doc"}


def test_show_details_message(capsys, tmp_path):
    temp_file = tmp_path / "test_file.txt"
    temp_file.write_text("Test content")
    context = {"base_path": str(temp_file)}
    show_details(context)
    captured = capsys.readouterr()
    assert captured.out == (
        "File name: test_file.txt\n"
        "File size in bytes: 12\n"
        "File type: file\n"
        "File extension: .txt\n"
        f"Last modified date: {date.today()}\n"
    )


def test_show_details_wrong_path(capsys, bad_context):
    show_details(bad_context)
    captured = capsys.readouterr()
    assert captured.out == "File 'test_file.doc' does not exist\n"


def test_show_details_non_existing_file(capsys):
    context = {"base_path": "test_trybe_file.txt"}
    show_details(context)
    captured = capsys.readouterr()
    assert captured.out == "File 'test_trybe_file.txt' does not exist\n"


def test_show_details_without_extension(capsys, tmp_path):
    temp_file = tmp_path / "test"
    temp_file.write_text("teste")
    context = {"base_path": str(temp_file)}
    show_details(context)
    captured = capsys.readouterr()
    print("captured.out:", captured.out)
    assert captured.out == (
        f"File name: test\n"
        f"File size in bytes: 5\n"
        f"File type: file\n"
        f"File extension: [no extension]\n"
        f"Last modified date: {date.today()}\n"
    )
