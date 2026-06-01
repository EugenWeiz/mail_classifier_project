import pytest
from mail_classifier.email_parser import parse_email_text

@pytest.fixture
def empty_email_template():
    return {
        "sender": "",
        "recipient": "",
        "subject": "",
        "body": "",
    }


def test_none_input(empty_email_template):
    assert parse_email_text(None) == empty_email_template

def test_empty_input(empty_email_template):
    assert parse_email_text("") == empty_email_template

def test_no_headers():
    text = "Привет! У меня сломался ноутбук! Пока!"
    result = parse_email_text(text)
    assert result["sender"] == ""
    assert result["recipient"] == ""
    assert result["subject"] == ""
    assert result["body"] == text

def test_duplicate_in_header():
    text = ("From: Вероничка Неничка <v.volodina@company.ru> \n"
            "From: Невероничка Ничка <v.anoxina@company.ru> \n")
    result = parse_email_text(text)
    assert result["sender"] == "Вероничка Неничка <v.volodina@company.ru>"
    assert result["recipient"] == ""
    assert result["subject"] == ""
    assert result["body"] == ""

def test_uppercase_prefixes():
    text = "FROM: NOTFOUND@CORP.LOCAL\n TO: IT-SUPPORT@COMPANT.RU \n SUBJECT: WE LOVE HSE\n"
    result = parse_email_text(text)
    assert result["sender"] == "NOTFOUND@CORP.LOCAL"
    assert result["recipient"] == "IT-SUPPORT@COMPANT.RU"
    assert result["subject"] == "WE LOVE HSE"
    assert result["body"] == ""

def test_different_line_endings():
    text = "From: programmerEnthusiast@hse.com\r\nTo: testerEnthusiast@hse.com\rSubject: HappyHouse\r\n\r\nHello\rWorld"
    result = parse_email_text(text)
    assert result["sender"] == "programmerEnthusiast@hse.com"
    assert result["recipient"] == "testerEnthusiast@hse.com"
    assert result["subject"] == "HappyHouse"
    assert result["body"] == "Hello\nWorld"

def test_whitespace_trimming():
    text = "  From:   imoportantWorker@test.com   \n to:     bigBoss@test.com     "
    result = parse_email_text(text)
    assert result["sender"] == "imoportantWorker@test.com"
    assert result["recipient"] == "bigBoss@test.com"
    assert result["subject"] == ""
    assert result["body"] == ""

def test_russian_headers():
    text = "От: Андрей Николаевич\n" "Кому: Дмитрий Александрович\n" "Тема: Комиссия по математическому анализу\n"
    result = parse_email_text(text)
    assert result["sender"] == "Андрей Николаевич"
    assert result["recipient"] == "Дмитрий Александрович"
    assert result["subject"] == "Комиссия по математическому анализу"
    assert result["body"] == ""

def test_header_prefix_inside_body():
    text = ("From: Наталья Великолепная <bedabeda.problemaproblema@corp.local>\n Кажется From: Наталья Великолепная возникла беда беда и проблема проблема")
    result = parse_email_text(text)
    assert result["sender"] == "Наталья Великолепная <bedabeda.problemaproblema@corp.local>"
    assert result["recipient"] == ""
    assert result["subject"] == ""
    assert result["body"] == "Кажется From: Наталья Великолепная возникла беда беда и проблема проблема"
