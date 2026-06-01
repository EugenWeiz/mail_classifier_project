import pytest
from mail_classifier.text_normalizer import (is_russian_word, normalize_russian_word, normalize_text, normalize_email_fields)

@pytest.fixture
def session_email():
    return {
        "sender": "students@edu.hse.ru",
        "recipient": "sanochkin@edu.ru",
        "subject": "СЕССИЯ... Пупупупу МАТАН СПАСИТЕ",
        "body": "Саночкин, пощади! Зачеты и экзамены близко",
    }

@pytest.fixture
def incomplete_session_email():
    return {
        "subject": "МАТАН",
    }


def test_is_russian_word_true():
    assert is_russian_word("сессия") is True

def test_is_russian_word_false_for_english_word():
    assert is_russian_word("hse") is False

def test_is_russian_word_true_for_mixed_word():
    assert is_russian_word("hseматан") is True

def test_normalize_russian_word_session():
    result = normalize_russian_word("экзамены")
    assert result == "экзамен"

def test_normalize_russian_word_replaces_yo():
    result = normalize_russian_word("зачёты")
    assert result == "зачет"

def test_normalize_text_none():
    result = normalize_text(None)
    assert result == []

def test_normalize_text_empty_string():
    result = normalize_text("")
    assert result == []

def test_normalize_text_session_phrase():
    result = normalize_text("Сессия... Пупупупу МАТАН СПАСИТЕ")
    assert "сессия" in result
    assert "пупупуп" in result
    assert "матан" in result
    assert "спасти" in result

def test_normalize_text_laugh_and_teacher_phrase():
    result = normalize_text("Саночкин, пощади!")
    assert "саночкин" in result

def test_normalize_text_english_words_and_numbers():
    result = normalize_text("HSE LMS 401 MATAN 2026")
    assert result == ["hse", "lms", "401", "matan", "2026"]

def test_normalize_text_replaces_yo_before_tokenization():
    result = normalize_text("Зачёты")
    assert result == ["зачет"]

def test_normalize_email_fields(session_email):
    result = normalize_email_fields(session_email)
    assert result["sender"] == ["students", "edu", "hse", "ru"]
    assert result["recipient"] == ["sanochkin", "edu", "ru"]
    assert "сессия" in result["subject"]
    assert "пупупуп" in result["subject"]
    assert "матан" in result["subject"]
    assert "спасти" in result["subject"]
    assert "саночкин" in result["body"]
    assert "зачет" in result["body"]
    assert "экзамен" in result["body"]

def test_normalize_email_fields_with_missing_fields(incomplete_session_email):
    result = normalize_email_fields(incomplete_session_email)
    assert result["sender"] == []
    assert result["recipient"] == []
    assert result["subject"] == ["матан"]
    assert result["body"] == []
