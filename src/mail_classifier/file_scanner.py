import os

from .rules import SYSTEM_FILE_NAMES

# функция, которая ищет файлы во входящей папке
def scan_files(input_directory):
    result = {
        "success": False,
        "files": [],
        "skipped_directories": [],
        "skipped_system_files": [],
        "error_type": "",
        "error_message": "",
    }

    try:
        items = sorted(os.listdir(input_directory))
    except FileNotFoundError:
        result["error_type"] = "input_directory_not_found"
        result["error_message"] = f"Папка {input_directory} не найдена"
        return result
    except NotADirectoryError:
        result["error_type"] = "input_path_is_not_directory"
        result["error_message"] = f"{input_directory} не является папкой"
        return result
    except OSError as error:
        result["error_type"] = "scan_error"
        result["error_message"] = f"Не удалось прочитать папку {input_directory}, возникла ошибка: {error}"
        return result

    for item in items:
        item_path = os.path.join(input_directory, item)

        if item in SYSTEM_FILE_NAMES:
            result["skipped_system_files"].append(item_path)
        elif os.path.isfile(item_path):
            result["files"].append(item_path)
        elif os.path.isdir(item_path):
            result["skipped_directories"].append(item_path)

    result["success"] = True
    return result
