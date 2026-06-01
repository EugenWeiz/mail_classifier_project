from .file_scanner import scan_files
from .email_reader import read_email_file
from .email_parser import parse_email_text
from .text_normalizer import normalize_email_fields
from .classifier import classify_email
from .router import route_file
from .reporter import create_report, add_file_result, save_report

INPUT_DIRECTORY = "data/inbox"
OUTPUT_DIRECTORY = "data/output"
REPORTS_DIRECTORY = "reports"

def process_file(file_path, report):
    read_result = read_email_file(file_path)

    if not read_result["success"]:
        category = read_result["category"]
        classification_result = {}
    else:
        parsed_email = parse_email_text(read_result["text"])
        normalized_email = normalize_email_fields(parsed_email)
        classification_result = classify_email(normalized_email)
        category = classification_result["category"]

    route_result = route_file(
        file_path = file_path,
        output_directory = OUTPUT_DIRECTORY,
        category = category,
    )

    add_file_result(
        report = report,
        file_path = file_path,
        category = category,
        route_result = route_result,
        read_result = read_result,
        classification_result = classification_result,
    )

def main():
    print("Запуск обработки писем")

    scan_result = scan_files(INPUT_DIRECTORY)
    if not scan_result["success"]:
        print("Ошибка сканирования входящей папки")
        print(scan_result["error_message"])
        return

    files = scan_result["files"]
    print(f"Найдено файлов: {len(files)}")
    print(f"Пропущено системных файлов: {len(scan_result['skipped_system_files'])}")
    print(f"Пропущено папок: {len(scan_result['skipped_directories'])}")

    report = create_report()
    for file_path in files:
        process_file(file_path, report)
    save_result = save_report(report, REPORTS_DIRECTORY)

    print("")
    print("Обработка завершена")
    print(f"Всего обработано файлов: {report['total_files']}")
    print(f"Успешно перемещено: {report['successful_routes']}")
    print(f"Ошибок перемещения: {report['failed_routes']}")

    if save_result["success"]:
        print(f"Отчёт сохранён: {save_result['report_path']}")
    else:
        print("Не удалось сохранить отчёт")
        print(save_result["error_message"])

if __name__ == "__main__":
    main()
