import re
import pymorphy3

morph = pymorphy3.MorphAnalyzer()
WORD_PATTERN = re.compile(r"[a-zа-я0-9]+", re.IGNORECASE)

def is_russian_word(word):
    for c in word:
        if "а" <= c <= "я":
            return True

    return False

def normalize_russian_word(word):
    normal_word = morph.parse(word)[0]
    normal_word = normal_word.normal_form
    normal_word = normal_word.replace("ё", "е")

    return normal_word

def normalize_email_fields(parsed_email):
    return {
        "sender": normalize_text(parsed_email.get("sender", "")),
        "recipient": normalize_text(parsed_email.get("recipient", "")),
        "subject": normalize_text(parsed_email.get("subject", "")),
        "body": normalize_text(parsed_email.get("body", "")),
    }

def normalize_text(text):
    if text is None:
        text = ""

    text = text.lower()
    words = WORD_PATTERN.findall(text)

    normalized_words = []
    for word in words:
        if is_russian_word(word):
            normalized_words.append(normalize_russian_word(word))
        else:
            normalized_words.append(word)

    return normalized_words
