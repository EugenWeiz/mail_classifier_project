import os

from .rules import (
    TEXT_EXTENSIONS,
    SYSTEM_FILE_NAMES,
    MAX_FILE_SIZE_BYTES,
    ENCODINGS_TO_TRY,
    QUARANTINE_REASONS,
)


# функция, которая безопасно читает текст письма из файла
def read_email_file(file_path):
    result = {
        "success": False,
        "file_path": file_path,
        "text": "",
        "encoding": "",
        "category": "",
        "quarantine_reason": "",
        "error_message": "",
    }

    # 1. Проверяем, существует ли путь
    if not os.path.exists(file_path):
        result["category"] = "technical_quarantine"
        result["quarantine_reason"] = "read_error"
        result["error_message"] = f"Файл не найден: {file_path}"
        return result

    # 2. Проверяем, что это именно файл, а не папка
    if not os.path.isfile(file_path):
        result["category"] = "technical_quarantine"
        result["quarantine_reason"] = "read_error"
        result["error_message"] = f"Путь не является файлом: {file_path}"
        return result

    file_name = os.path.basename(file_path)

    # 3. Проверяем системные файлы
    if file_name in SYSTEM_FILE_NAMES:
        result["category"] = "technical_quarantine"
        result["quarantine_reason"] = "unsupported_extension"
        result["error_message"] = f"{QUARANTINE_REASONS['unsupported_extension']}: {file_name}"
        return result

    # 4. Проверяем размер файлаа
    try:
        file_size = os.path.getsize(file_path)
    except OSError as error:
        result["category"] = "technical_quarantine"
        result["quarantine_reason"] = "read_error"
        result["error_message"] = f"{QUARANTINE_REASONS['read_error']}: {file_name}. Детали: {error}"
        return result

    if file_size == 0:
        result["category"] = "technical_quarantine"
        result["quarantine_reason"] = "empty_file"
        result["error_message"] = f"{QUARANTINE_REASONS['empty_file']}: {file_name}"
        return result

    if file_size > MAX_FILE_SIZE_BYTES:
        result["category"] = "technical_quarantine"
        result["quarantine_reason"] = "too_large"
        result["error_message"] = f"{QUARANTINE_REASONS['too_large']}: {file_name}"
        return result

    # 5. Проверяем расширение файла
    file_name_without_extension, extension = os.path.splitext(file_name)
    extension = extension.lower()

    if extension not in TEXT_EXTENSIONS:
        result["category"] = "technical_quarantine"
        result["quarantine_reason"] = "unsupported_extension"
        result["error_message"] = (f"{QUARANTINE_REASONS['unsupported_extension']}: {file_name}")
        return result

    # 6. Пробуем прочитат текстовый файл
    for encoding in ENCODINGS_TO_TRY:
        try:
            file = open(file_path, "r", encoding = encoding)
            text = file.read()

            if text.startswith("\ufeff"):
                text = text.replace("\ufeff", "", 1)

            if text.strip() == "":
                result["category"] = "technical_quarantine"
                result["quarantine_reason"] = "empty_file"
                result["error_message"] = f"{QUARANTINE_REASONS['empty_file']}: {file_name}"
                return result

            result["success"] = True
            result["text"] = text
            result["encoding"] = encoding
            return result

        except UnicodeDecodeError:
            continue

        except OSError as error:
            result["category"] = "technical_quarantine"
            result["quarantine_reason"] = "read_error"
            result["error_message"] = f"{QUARANTINE_REASONS['read_error']}: {file_name}. Детали: {error}"
            return result

    # 7. Если ни одна кодировка не подошла
    result["category"] = "technical_quarantine"
    result["quarantine_reason"] = "read_error"
    result["error_message"] = (f"{QUARANTINE_REASONS['read_error']}: "f"{file_name}. Не удалось прочитать файл в поддерживаемых кодировках")
    return result
