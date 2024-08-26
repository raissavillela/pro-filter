from pro_filer.actions.main_actions import show_disk_usage


def test_show_disk_usage_single_file(tmp_path, capsys, monkeypatch):
    file_1 = tmp_path / "file1.txt"
    file_1.write_text("Hello World")

    context = {"all_files": [str(file_1)]}

    monkeypatch.setattr(
        "pro_filer.actions.main_actions._get_printable_file_path", lambda x: x
    )

    show_disk_usage(context)
    captured = capsys.readouterr()

    expected_output = f"'{file_1}':".ljust(70) + " 11 (100%)\nTotal size: 11\n"
    assert captured.out == expected_output


def test_show_disk_usage_multiple_files(tmp_path, capsys, monkeypatch):
    file_1 = tmp_path / "file1.txt"
    file_1.write_text("Hello World")

    file_2 = tmp_path / "file2.txt"
    file_2.write_text("Hello")

    context = {"all_files": [str(file_1), str(file_2)]}

    monkeypatch.setattr(
        "pro_filer.actions.main_actions._get_printable_file_path", lambda x: x
    )

    show_disk_usage(context)
    captured = capsys.readouterr()

    output = captured.out.split("\n")
    assert output[0].startswith(f"'{file_1}':".ljust(70))
    assert output[1].startswith(f"'{file_2}':".ljust(70))
    assert "Total size: 16" in captured.out


def test_show_disk_usage_no_files(capsys):
    context = {"all_files": []}

    show_disk_usage(context)
    captured = capsys.readouterr()

    assert captured.out == "Total size: 0\n"
