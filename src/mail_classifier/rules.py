# Файл с основными правилами классификации писем.

# 1. Категории
CATEGORIES = [
    "incidents_and_alerts",
    "access_and_user_accounts",
    "hardware_requests",
    "software_issues",
    "client_partner_requests",
    "docs_finance_contracts",
    "org_info_and_meetings",
    "security_spam_phishing",
    "needs_manual_review",
    "technical_quarantine",
]

CATEGORY_TITLES = {
    "incidents_and_alerts": "Инциденты и уведомления мониторинга",
    "access_and_user_accounts": "Доступы и учётные записи",
    "hardware_requests": "Оборудование и техника",
    "software_issues": "Проблемы с программами",
    "client_partner_requests": "Клиенты и партнёры",
    "docs_finance_contracts": "Документы, финансы и договоры",
    "org_info_and_meetings": "Организационные письма и встречи",
    "security_spam_phishing": "Спам и подозрительные письма",
    "needs_manual_review": "Требует ручного разбора",
    "technical_quarantine": "Технический карантин",
}


# 2. Веса и пороги классификации
MARKER_WEIGHTS = {
    "common": 1,
    "strong": 4,
}

FIELD_WEIGHTS = {
    "subject": 2,
    "body": 1,
    "sender": 1,
}

MIN_SCORE = 4
MIN_SCORE_GAP = 2

# 3. Правила технического карантина
TEXT_EXTENSIONS = [
    ".txt",
]

SYSTEM_FILE_NAMES = [
    ".DS_Store",
]

MAX_FILE_SIZE_BYTES = 1_048_576

ENCODINGS_TO_TRY = [
    "utf-8",
    "utf-8-sig",
    "cp1251",
]

QUARANTINE_REASONS = {
    "empty_file": "Пустой файл",
    "too_large": "Слишком большой файл",
    "unsupported_extension": "Неподдерживаемое расширение",
    "read_error": "Ошибка чтения файла",
}

# 4. Настройки отчёта и логов
LOG_FILE_NAME = "processing.log"
SUMMARY_REPORT_FILE_NAME = "summary_report.txt"

# 5. Маркеры категорий
CATEGORY_MARKERS = {
    "incidents_and_alerts": {
        "common": [
            "сервис",
            "сервер",
            "ошибка",
            "статус",
            "эскалация",
            "коллега",
            "отдел",
            "метрика",
            "cpu",
            "disk",
            "uptime",
        ],
        "strong": [
            "инцидент",
            "сбой",
            "критичный",
            "недоступный",
            "остановить",
            "мониторинг",
            "healthcheck",
            "alert",
            "warning",
            "critical",
            "threshold",
            "gateway",
            "cluster",
            "database",
            "5xx",
            "500",
        ],
    },

    "access_and_user_accounts": {
        "common": [
            "доступ",
            "право",
            "роль",
            "группа",
            "аккаунт",
            "учетный",
            "запись",
            "сотрудник",
            "почта",
            "перевод",
            "руководитель",
            "vpn",
            "gitlab",
            "confluence",
            "1c",
            "bi",
            "портал",
        ],
        "strong": [
            "onboarding",
            "offboarding",
            "увольнение",
            "выдать",
            "предоставить",
            "восстановить",
            "отключить",
            "добавить",
        ],
    },

    "hardware_requests": {
        "common": [
            "ноутбук",
            "монитор",
            "экран",
            "мышь",
            "клавиатура",
            "гарнитура",
            "принтер",
            "сканер",
            "картридж",
            "устройство",
            "периферия",
            "ремонт",
            "замена",
            "диагностика",
        ],
        "strong": [
            "сломаться",
            "сломанный",
            "падение",
            "включаться",
            "печатать",
            "сканировать",
            "определяться",
        ],
    },

    "software_issues": {
        "common": [
            "программа",
            "приложение",
            "браузер",
            "версия",
            "обновление",
            "установщик",
            "файл",
            "chrome",
            "outlook",
            "zoom",
            "excel",
            "adobe",
            "reader",
            "антивирус",
        ],
        "strong": [
            "запускаться",
            "открываться",
            "устанавливаться",
            "зависать",
            "зависнуть",
            "переустановка",
        ],
    },

    "client_partner_requests": {
        "common": [
            "клиент",
            "партнер",
            "контрагент",
            "тикет",
            "заявка",
            "портал",
            "кабинет",
            "регистрация",
            "интеграция",
            "внешний",
        ],
        "strong": [
            "api",
            "unauthorized",
            "401",
            "жалоба",
        ],
    },

    "docs_finance_contracts": {
        "common": [
            "документ",
            "договор",
            "акт",
            "счет",
            "оплата",
            "платеж",
            "реквизит",
            "тз",
            "подпись",
            "комментарий",
            "замечание",
            "правка",
            "инструкция",
            "приложение",
        ],
        "strong": [
            "финальный",
            "закрывающий",
            "выполненный",
            "подписать",
        ],
    },

    "org_info_and_meetings": {
        "common": [
            "отпуск",
            "больничный",
            "график",
            "дайджест",
            "созвон",
            "встреча",
            "демо",
            "календарь",
            "статус",
            "задача",
            "плановый",
            "обновление",
            "портал",
        ],
        "strong": [
            "нетрудоспособность",
            "пригласить",
            "перенос",
        ],
    },

    "security_spam_phishing": {
        "common": [
            "пароль",
            "логин",
            "карта",
            "приз",
            "розыгрыш",
            "скидка",
            "ссылка",
            "verification",
            "offer",
            "winner",
        ],
        "strong": [
            "заблокировать",
            "верификация",
            "личность",
            "выиграть",
            "exclusive",
            "urgent",
            "password",
        ],
    },

    "needs_manual_review": {
        "common": [
            "помогите",
            "проблема",
            "срочно",
            "вложение",
        ],
        "strong": [
            "непонятно",
            "???",
        ],
    },
}
