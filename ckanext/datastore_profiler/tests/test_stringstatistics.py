"""
Test module for stringsatistics module using pytest

Test following methods under StringStatistics class:
- unique_count
- mask_count
- word_count

Contain following functions:
- test_unique_string_counts_from_list
- test_unique_mask_counts_from_list
- test_unique_word_counts_from_list
- test_word_stats_from_list
"""

# User defined modules
from utils.stringstatistics import StringStatistics

test_data = [
    "val2",
    "val3",
    "val4",
    "ccc-9",
    "d-1",
    "val-3",
    "val-3",
    "val1 val2 val3",
    "this is val1",
    "this is val2",
    None,
    None,
]


def test_unique_string_counts_from_list():
    """
    Test unique strings count
    """

    # get stats from appropriate class
    dict_stats = StringStatistics().unique_count(test_data)["counts"]

    # set the expected results
    correct_stats = {
        "val-3": 2,
        None: 2,
        "Value Empty/Null": 2,
        "val3": 1,
        "ccc-9": 1,
        "this is val2": 1,
        "d-1": 1,
        "val1 val2 val3": 1,
        "this is val1": 1,
        "val4": 1,
        "val2": 1,
    }

    # assert response
    assert dict_stats == correct_stats


def test_unique_mask_counts_from_list():
    """
    Test unique string mask/formatting count
    """

    # get stats from appropriate class
    dict_stats = StringStatistics().mask_count(test_data)["counts"]

    # set the expected results
    correct_stats = {
        "LLLD": 3,
        "LLL-D": 3,
        "LLLL LL LLLD": 2,
        "null_count": 2,
        "L-D": 1,
        "LLLD LLLD LLLD": 1,
    }

    # assert response
    assert dict_stats == correct_stats


def test_unique_word_counts_from_list():
    """
    Test unique words count excluding stop words
    """

    # get stats from appropriate class
    dict_stats = StringStatistics().word_count(test_data)["word_counts"]

    # set the expected results
    correct_stats = {
        "val2": 3,
        "val-3": 2,
        "val3": 2,
        "val1": 2,
        "is": 2,
        "Value Empty/Null": 2,
        "ccc-9": 1,
        "d-1": 1,
        "val4": 1,
    }

    # assert response
    assert dict_stats == correct_stats


def test_word_stats_from_list():
    """
    Test min and max count and min and max of the strings length
    """

    # get stats from appropriate class
    dict_stats = StringStatistics().word_count(test_data)

    # set the expected results
    correct_stats = {
        "min_word_count": 1,
        "max_word_count": 3,
        "min_string_length": 3,
        "max_string_length": 14,
    }

    # assert responses
    assert dict_stats["min_word_count"] == correct_stats["min_word_count"]
    assert dict_stats["max_word_count"] == correct_stats["max_word_count"]
