from .rules import (
    CATEGORY_MARKERS,
    MARKER_WEIGHTS,
    FIELD_WEIGHTS,
    MIN_SCORE,
    MIN_SCORE_GAP,
)


def create_empty_scores():
    scores = {}
    for category in CATEGORY_MARKERS:
        scores[category] = 0

    return scores

def create_empty_markers():
    markers = {}
    for category in CATEGORY_MARKERS:
        markers[category] = []

    return markers

def add_scores_for_field(words, field_name, field_weight, scores, markers):
    for category, category_markers in CATEGORY_MARKERS.items():
        for marker_type, category_words in category_markers.items():
            marker_weight = MARKER_WEIGHTS[marker_type]

            for marker in category_words:
                if marker in words:
                    count = words.count(marker)
                    score = marker_weight * field_weight * count
                    scores[category] += score

                    markers[category].append({
                        "marker": marker,
                        "type": marker_type,
                        "field": field_name,
                        "count": count,
                        "score": score,
                    })


def classify_email(normalized_email):
    result = {
        "category": "needs_manual_review",
        "scores": {},
        "markers": {},
        "reason": "",
    }

    if normalized_email is None:
        result["reason"] = "Нет данных для классификации"
        return result

    scores = create_empty_scores()
    markers = create_empty_markers()
    for field_name, field_weight in FIELD_WEIGHTS.items():
        words = normalized_email.get(field_name, [])

        add_scores_for_field(words = words,
                             field_name = field_name,
                             field_weight = field_weight,
                             scores = scores,
                             markers = markers)

    result["scores"], result["markers"] = scores, markers

    sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse = True)
    best_category, best_score  = sorted_scores[0][0], sorted_scores[0][1]
    second_category, second_score = sorted_scores[1][0], sorted_scores[1][1]

    if best_score < MIN_SCORE:
        result["category"] = "needs_manual_review"
        result["reason"] = (f"Лучший результат слишком низкий: {best_category} набрала {best_score} баллов")
        return result

    if second_score > 0 and best_score - second_score < MIN_SCORE_GAP:
        result["category"] = "needs_manual_review"
        result["reason"] = (f"Нет явного лидера: {best_category} набрала {best_score} баллов, {second_category} набрала {second_score} баллов")
        return result

    result["category"] = best_category
    result["reason"] = (f"Категория {best_category} набрала больше всего баллов: {best_score}")
    return result
