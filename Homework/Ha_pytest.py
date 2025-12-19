import pytest


def count_word_matches(text, target):
    """
    Zählt, wie oft ein Zielwort als eigenständiges Wort im Text vorkommt.
    Die Übereinstimmung erfolgt ohne Berücksichtigung der Groß-/Kleinschreibung,
    und Wörter sind durch Leerzeichen getrennt.

    Args:
        text (str): Eingabetext, in dem gesucht wird.
        target (str): Das gesuchte Wort.

    Returns:
        int: Anzahl der Vorkommen des Zielwortes als eigenständiges Wort.
    """
    if not text or not target:
        return 0

    # Text in Wörter aufteilen und für case-insensitive Vergleich in Kleinbuchstaben umwandeln
    words = text.lower().split()
    target = target.lower()

    # Eigenständige Vorkommen des Zielwortes zählen
    return words.count(target)


# Übung 1: Basis-Tests
@pytest.mark.parametrize("text, target, expected_result", [
    (None, "word", 0),
    ("hello world", None, 0),
    ("The cat sat on the mat", "cat", 1),
    ("Dog dog DOG dOg", "dog", 4),
    ("hello hello HELLO", "hello", 3),
    ("No matches here", "yes", 0),
    ("catcat cat catdog", "cat", 1),
    ("a a a", "a", 3)
])


def test_parametrize(text, target, expected_result):
    # zu testende Funktion
    actual_result = count_word_matches(text, target)

    # tatsächliches gegen erwartetes Ergebnis
    assert actual_result == expected_result


# Übung 2: Testen von Randfällen (Edge Case Testing)
@pytest.fixture
def edge_case_inputs():

    return {
        "empty_text": ("", "word", 0),                          # 1
        "empty_target": ("hello world", "", 0),                 # 2
        "both_empty": ("", "", 0),                              # 3
        "multiple_spaces": ("hello   world", "world", 1),       # 4
        "leading_trailing_spaces": ("  cat  ", "cat", 1),       # 5
        "punctuation_not_separator": ("cat,dog cat", "cat", 1), # 6
        "single_char": ("x y z", "x", 1),                       # 7
    }


def test_count_word_matches(edge_case_data):
    text, target, expected_result = edge_case_data
    assert count_word_matches(text, target) == expected_result


# Übung 3: Negativtests (Negative Testing)
@pytest.fixture(params=[
    # text, target, expected result
    (123, "word", AttributeError),
    ("hello world", 456, AttributeError),
    (["hello", "world"], "word", AttributeError),
    ("hello world", ["word"], AttributeError),
])


def invalid_input_data(request):
    return request.param


def test_count_word_matches_invalid_inputs(invalid_input_data):
    text, target, expected_result = invalid_input_data

    with pytest.raises(expected_result):
        count_word_matches(text, target)