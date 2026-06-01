import pytest
import os
from mail_classifier.file_scanner import scan_files

@pytest.fixture
def empty_directory(tmp_path):
    return tmp_path


@pytest.fixture
def filled_directory(tmp_path):
    file1 = os.path.join(str(tmp_path), "СекретныйФайл1.txt")
    file2 = os.path.join(str(tmp_path), "СекретныйФайл2.txt")
    with open(file1, "w", encoding="utf-8") as file:
        file.write("СекретнаяИнформация1")
    with open(file2, "w", encoding="utf-8") as file:
        file.write("СекретнаяИнформация2")
    return tmp_path


@pytest.fixture
def directory_with_subdirectory(tmp_path):
    file1 = os.path.join(str(tmp_path), "СекретныйФайл1.txt")
    subdirectory = os.path.join(str(tmp_path), "СекретнаяПодпапочка1")
    with open(file1, "w", encoding="utf-8") as file:
        file.write("СекретнаяИнформация1")
    os.mkdir(subdirectory)
    return tmp_path


def test_empty_directory_functioning(empty_directory):
    result = scan_files(str(empty_directory))
    assert result["success"] is True
    assert result["files"] == []
    assert result["skipped_directories"] == []
    assert result["skipped_system_files"] == []
    assert result["error_type"] == ""
    assert result["error_message"] == ""


def test_filled_directory_finds_files(filled_directory):
    result = scan_files(str(filled_directory))
    expected_file1 = os.path.join(str(filled_directory), "СекретныйФайл1.txt")
    expected_file2 = os.path.join(str(filled_directory), "СекретныйФайл2.txt")
    assert result["success"] is True
    assert result["files"] == [expected_file1, expected_file2]


def test_subdirectory_skipped(directory_with_subdirectory):
    result = scan_files(str(directory_with_subdirectory))
    expected_subdirectory = os.path.join(str(directory_with_subdirectory), "СекретнаяПодпапочка1")
    assert result["success"] is True
    assert result["skipped_directories"] == [expected_subdirectory]


def test_file_not_found_error(tmp_path):
    invalid_path = os.path.join(str(tmp_path), "CекретнаяПапка")
    result = scan_files(invalid_path)
    assert result["success"] is False
    assert result["error_type"] == "input_directory_not_found"
    assert result["error_message"] == f"Папка {invalid_path} не найдена"


def test_not_a_directory_error(tmp_path):
    file_path = os.path.join(str(tmp_path), "НеприметныйФайл.txt")
    with open(file_path, "w") as f:
        f.write("СекретнаяИнформация")
    result = scan_files(file_path)
    assert result["success"] is False
    assert result["error_type"] == "input_path_is_not_directory"
    assert result["error_message"] == f"{file_path} не является папкой"


def test_os_error_branch(monkeypatch, tmp_path):
    input_directory = str(tmp_path)

    def bad_listdir(_):
        raise OSError("вылезла ошибочка")
    monkeypatch.setattr(os, "listdir", bad_listdir)
    result = scan_files(input_directory)
    assert result["success"] is False
    assert result["error_type"] == "scan_error"
    assert result["error_message"] == f"Не удалось прочитать папку {input_directory}, возникла ошибка: вылезла ошибочка"


@pytest.mark.parametrize(
    "file_count",
    [1, 3, 5, 10]
)
def test_various_file_counts(tmp_path, file_count):
    expected_files = []
    for i in range(file_count):
        file_path = os.path.join(str(tmp_path), f"СекретныйФайл{i}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"СекретнаяИнформация{i}")
        expected_files.append(str(file_path))
    result = scan_files(str(tmp_path))
    assert result["success"] is True
    assert result["files"] == sorted(expected_files)
