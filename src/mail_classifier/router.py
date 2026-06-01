import os
from .rules import CATEGORIES

# функция, которая перемещает файл в папку выбранной категории
def route_file(file_path, output_directory, category):
    result = {
        "success": False,
        "source_path": file_path,
        "destination_path": "",
        "category": category,
        "error_message": "",
    }

    if category not in CATEGORIES:
        category = "needs_manual_review"
        result["category"] = category

    if not os.path.exists(file_path):
        result["error_message"] = f"Файл не найден: {file_path}"
        return result

    if not os.path.isfile(file_path):
        result["error_message"] = f"Путь не является файлом: {file_path}"
        return result

    category_directory = os.path.join(output_directory, category)

    try:
        os.makedirs(category_directory, exist_ok = True)
    except OSError as error:
        result["error_message"] = f"Не удалось создать папку {category_directory}: {error}"
        return result

    file_name = os.path.basename(file_path)
    destination_path = os.path.join(category_directory, file_name)
    destination_path = get_unique_path(destination_path)

    try:
        os.replace(file_path, destination_path)
    except OSError as error:
        result["error_message"] = f"Не удалось переместить файл {file_name}: {error}"
        return result

    result["success"] = True
    result["destination_path"] = destination_path
    return result

# функция, которая создаёт уникальный путь, если файл с таким именем уже существует
def get_unique_path(path):
    if not os.path.exists(path):
        return path

    directory = os.path.dirname(path)
    file_name = os.path.basename(path)
    name_without_extension, extension = os.path.splitext(file_name)
    counter = 1

    while True:
        new_file_name = f"{name_without_extension}_{counter}{extension}"
        new_path = os.path.join(directory, new_file_name)

        if not os.path.exists(new_path):
            return new_path

        counter += 1
