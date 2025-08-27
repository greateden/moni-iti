import pytest

from wordchain.utils import word_value


def test_word_value_basic():
    assert word_value("abc") == 1 + 2 + 3


def test_word_value_ignores_case_and_nonletters():
    assert word_value("Hello!") == word_value("hello")
    assert word_value("123") == 0
