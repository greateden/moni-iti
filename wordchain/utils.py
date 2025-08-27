"""Utility helpers for computing the numeric value of words."""

import string

ALPHABET = {ch: idx for idx, ch in enumerate(string.ascii_lowercase, start=1)}


def word_value(word: str) -> int:
    """Compute a deterministic numeric value for a word.

    The value is the sum of alphabetical positions of its letters.
    Non-letter characters are ignored. The function is case-insensitive.

    Parameters
    ----------
    word: str
        Input word to evaluate.

    Returns
    -------
    int
        Numeric value of the word.
    """
    return sum(ALPHABET.get(ch, 0) for ch in word.lower())
