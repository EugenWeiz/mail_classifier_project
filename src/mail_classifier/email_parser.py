# Модуль для выделения структуры письма.

HEADER_PREFIXES = {
    "sender": ["from:", "от:"],
    "recipient": ["to:", "кому:"],
    "subject": ["subject:", "тема:"],
}

def parse_email_text(raw_text):
    result = {
        "sender": "",
        "recipient": "",
        "subject": "",
        "body": "",
    }

    if raw_text is None:
        raw_text = ""

    raw_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = raw_text.split("\n")
    body_lines = []

    for line in lines:
        stripped_line = line.strip()
        header_found = False

        for field_name, prefixes in HEADER_PREFIXES.items():
            for prefix in prefixes:
                if stripped_line.lower().startswith(prefix):
                    value = stripped_line[len(prefix):].strip()

                    # Если поле уже было найдено раньше, не перезаписываем его
                    if result[field_name] == "":
                        result[field_name] = value

                    header_found = True
                    break

            if header_found:
                break

        if not header_found:
            body_lines.append(line)

    result["body"] = "\n".join(body_lines).strip()

    return result
