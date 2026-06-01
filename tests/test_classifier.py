import pytest
from mail_classifier.classifier import (create_empty_scores, create_empty_markers, add_scores_for_field, classify_email)
from mail_classifier.rules import CATEGORY_MARKERS

@pytest.fixture
def scores_and_markers():
    return create_empty_scores(), create_empty_markers()

@pytest.fixture
def software_email():
    return {
        "sender": [],
        "recipient": [],
        "subject": ["не", "открываться", "excel"],
        "body": ["обновление", "программа", "зависать"],
    }

@pytest.fixture
def session_email_without_markers():
    return {
        "sender": ["students", "edu", "hse", "ru"],
        "recipient": ["sanochkin", "edu", "ru"],
        "subject": ["сессия", "пупупуп", "матан", "спасти"],
        "body": ["саночкин", "пощадить", "экзамен"],
    }

@pytest.fixture
def unclear_email():
    return {
        "sender": [],
        "recipient": [],
        "subject": [],
        "body": ["зависать", "excel", "выдать"],
    }


def test_create_empty_scores():
    result = create_empty_scores()
    assert set(result.keys()) == set(CATEGORY_MARKERS.keys())
    assert all(score == 0 for score in result.values())

def test_create_empty_markers():
    result = create_empty_markers()
    assert set(result.keys()) == set(CATEGORY_MARKERS.keys())
    assert all(markers == [] for markers in result.values())

def test_add_scores_for_field(scores_and_markers):
    scores, markers = scores_and_markers
    add_scores_for_field(
        words=["excel", "excel", "зависать"],
        field_name="body",
        field_weight=1,
        scores=scores,
        markers=markers,
    )

    assert scores["software_issues"] == 6
    assert len(markers["software_issues"]) == 2

def test_classify_email_none():
    result = classify_email(None)
    assert result["category"] == "needs_manual_review"
    assert result["reason"] == "Нет данных для классификации"

def test_classify_software_email(software_email):
    result = classify_email(software_email)
    assert result["category"] == "software_issues"
    assert result["scores"]["software_issues"] > 0
    assert "software_issues" in result["reason"]

def test_classify_email_without_markers_goes_to_manual_review(session_email_without_markers):
    result = classify_email(session_email_without_markers)
    assert result["category"] == "needs_manual_review"
    assert "Лучший результат слишком низкий" in result["reason"]

def test_classify_email_with_close_scores_goes_to_manual_review(unclear_email):
    result = classify_email(unclear_email)

    assert result["category"] == "needs_manual_review"
    assert result["scores"]["software_issues"] == 5
    assert result["scores"]["access_and_user_accounts"] == 4
    assert "Нет явного лидера" in result["reason"]

def test_classify_email_with_missing_fields():
    normalized_email = {"subject": ["excel", "зависать"]}

    result = classify_email(normalized_email)
    assert result["category"] == "software_issues"
    assert result["scores"]["software_issues"] == 10
