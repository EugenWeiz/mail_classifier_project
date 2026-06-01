import pytest
from mail_classifier.email_reader import read_email_file


@pytest.fixture
def test_files(tmp_path):
    files = {}

    files["utf8"] = tmp_path / "checkGoodFileUtf8.txt"
    files["utf8"].write_text("Старались ученики БИ2510 :(", encoding = "utf-8")

    files["utf8_with_bom"] = tmp_path / "checkGoodFileUtf8WithBom.txt"
    files["utf8_with_bom"].write_text("Какой-то текст", encoding = "utf-8-sig")

    files["cp1251"] = tmp_path / "checkGoodFileCp1251.txt"
    files["cp1251"].write_text("Субочев лучший! ахахахахахахахаха", encoding = "cp1251")

    files["empty"] = tmp_path / "empty.txt"
    files["empty"].write_text("", encoding = "utf-8")

    files["spaces"] = tmp_path / "spaces.txt"
    files["spaces"].write_text("   \n\t   \n", encoding = "utf-8")

    files["large"] = tmp_path / "large.txt"
    files["large"].write_text("a" * 1_048_577, encoding = "utf-8")

    files["wrong_extension"] = tmp_path / "letter.pdf"
    files["wrong_extension"].write_text("Да что ж такое... ;(", encoding = "utf-8")

    files["system_file"] = tmp_path / ".DS_Store"
    files["system_file"].write_text("system file", encoding = "utf-8")

    files["bad_encoding"] = tmp_path / "bad_encoding.txt"
    files["bad_encoding"].write_bytes(b"\x98\x98\x98")

    files["directory"] = tmp_path / "directory"
    files["directory"].mkdir()

    files["missing"] = tmp_path / "wrongFile.txt"

    return files



def test_nonexist_path_1():
    file_path = "Wrong path"
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "read_error"
    assert result["error_message"] == f"Файл не найден: {file_path}"


def test_nonexist_path_2(test_files):
    file_path = test_files["missing"]
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "read_error"
    assert result["error_message"] == f"Файл не найден: {file_path}"


def test_not_file(test_files):
    file_path = test_files["directory"]
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "read_error"
    assert result["error_message"] == f"Путь не является файлом: {file_path}"


def test_system_file(test_files):
    file_path = test_files["system_file"]
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "unsupported_extension"
    assert result["error_message"] == "Неподдерживаемое расширение: .DS_Store"


def test_getsize_OSError(monkeypatch, test_files):
    file_path = test_files["utf8"]

    def fake_getsize(path):
        raise OSError("Нельзя получить размер")

    monkeypatch.setattr("mail_classifier.email_reader.os.path.getsize", fake_getsize)
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "read_error"
    assert result["error_message"] == "Ошибка чтения файла: checkGoodFileUtf8.txt. Детали: Нельзя получить размер"


def test_open_OSError(monkeypatch, test_files):
    file_path = test_files["utf8"]

    def fake_open(path, mode, encoding):
        raise OSError("Нельзя открыть")

    monkeypatch.setattr("mail_classifier.email_reader.open", fake_open, raising = False)
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "read_error"
    assert result["error_message"] == "Ошибка чтения файла: checkGoodFileUtf8.txt. Детали: Нельзя открыть"


def test_empty_file(test_files):
    file_path = test_files["empty"]
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "empty_file"
    assert result["error_message"] == "Пустой файл: empty.txt"


def test_space_file(test_files):
    file_path = test_files["spaces"]
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "empty_file"
    assert result["error_message"] == "Пустой файл: spaces.txt"


def test_large_test(test_files):
    file_path = test_files["large"]
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "too_large"
    assert result["error_message"] == "Слишком большой файл: large.txt"


def test_wrong_extension(test_files):
    file_path = test_files["wrong_extension"]
    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "unsupported_extension"
    assert result["error_message"] == "Неподдерживаемое расширение: letter.pdf"


def test_good_UTF8_file(test_files):
    file_path = test_files["utf8"]

    result = read_email_file(file_path)

    assert result["success"] is True
    assert result["file_path"] == file_path
    assert result["text"] == "Старались ученики БИ2510 :("
    assert result["encoding"] == "utf-8"


def test_good_CP1251_file(test_files):
    file_path = test_files["cp1251"]

    result = read_email_file(file_path)

    assert result["success"] is True
    assert result["file_path"] == file_path
    assert result["text"] == "Субочев лучший! ахахахахахахахаха"
    assert result["encoding"] == "cp1251"


def test_good_UTF8_SIG_file(test_files):
    file_path = test_files["utf8_with_bom"]

    result = read_email_file(file_path)

    assert result["success"] is True
    assert result["file_path"] == file_path
    assert result["text"] == "Какой-то текст"
    assert result["encoding"] == "utf-8"


def test_wrong_encoding(test_files):
    file_path = test_files["bad_encoding"]

    result = read_email_file(file_path)

    assert result["success"] is False
    assert result["file_path"] == file_path
    assert result["category"] == "technical_quarantine"
    assert result["quarantine_reason"] == "read_error"
    assert result["error_message"] == (
        "Ошибка чтения файла: bad_encoding.txt. "
        "Не удалось прочитать файл в поддерживаемых кодировках"
    )
