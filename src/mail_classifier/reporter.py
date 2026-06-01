import os
from .rules import (
    CATEGORIES,
    CATEGORY_TITLES,
    SUMMARY_REPORT_FILE_NAME,
)

# Создаёт пустой отчёт
def create_report():
    category_counts = {}
    for category in CATEGORIES:
        category_counts[category] = 0

    return {
        "total_files": 0,
        "successful_routes": 0,
        "failed_routes": 0,
        "category_counts": category_counts,
        "records": [],
    }


# Добавляем в отчёт результат обработки одного файла
def add_file_result(report, file_path, category, route_result, read_result=None, classification_result=None):
    file_name = os.path.basename(file_path)
    if read_result is None:
        read_result = {}

    if classification_result is None:
        classification_result = {}

    route_success = route_result.get("success", False)
    destination_path = route_result.get("destination_path", "")
    route_error = route_result.get("error_message", "")
    reason = classification_result.get("reason", "")
    if read_result.get("quarantine_reason", "") != "":
        reason = read_result.get("error_message", "")
    record = {
        "file_name": file_name,
        "source_path": file_path,
        "destination_path": destination_path,
        "category": category,
        "route_success": route_success,
        "reason": reason,
        "error_message": route_error,
    }

    report["records"].append(record)
    report["total_files"] += 1
    if route_success:
        report["successful_routes"] += 1
    else:
        report["failed_routes"] += 1
    if category not in report["category_counts"]:
        report["category_counts"][category] = 0

    report["category_counts"][category] += 1


# Формирует текст итогового отчёта
def format_report(report):
    lines = []
    lines.append("ИТОГОВЫЙ ОТЧЁТ ПО ОБРАБОТКЕ ПИСЕМ")
    lines.append("=" * 45)
    lines.append("")
    lines.append(f"Всего файлов обработано: {report['total_files']}")
    lines.append(f"Успешно перемещено: {report['successful_routes']}")
    lines.append(f"Ошибок перемещения: {report['failed_routes']}")
    lines.append("")
    lines.append("РАСПРЕДЕЛЕНИЕ ПО КАТЕГОРИЯМ")
    lines.append("-" * 45)
    for category, count in report["category_counts"].items():
        if count > 0:
            title = CATEGORY_TITLES.get(category, category)
            lines.append(f"{title}: {count}")
    lines.append("")
    lines.append("ДЕТАЛИ ПО ФАЙЛАМ")
    lines.append("-" * 45)
    for record in report["records"]:
        lines.append(f"Файл: {record['file_name']}")
        lines.append(f"Категория: {record['category']}")
        if record["route_success"]:
            lines.append("Статус: перемещён")
            lines.append(f"Куда перемещён: {record['destination_path']}")
        else:
            lines.append("Статус: ошибка перемещения")
            lines.append(f"Ошибка: {record['error_message']}")
        if record["reason"] != "":
            lines.append(f"Причина: {record['reason']}")
        lines.append("")
    return "\n".join(lines)


# Cохраняет отчёт в файл
def save_report(report, output_directory):
    result = {
        "success": False,
        "report_path": "",
        "error_message": "",
    }

    try:
        os.makedirs(output_directory, exist_ok=True)
    except OSError as error:
        result["error_message"] = f"Не удалось создать папку для отчёта: {error}"
        return result

    report_path = os.path.join(output_directory, SUMMARY_REPORT_FILE_NAME)
    try:
        report_text = format_report(report)
        with open(report_path, "w", encoding="utf-8") as file:
            file.write(report_text)
    except OSError as error:
        result["error_message"] = f"Не удалось сохранить отчёт: {error}"
        return result

    result["success"] = True
    result["report_path"] = report_path
    return result
