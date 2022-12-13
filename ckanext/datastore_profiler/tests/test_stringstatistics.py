"""
Test module for stringsatistics module using pytest

Test following methods under StringStatistics class:
- unique_count
- mask_count
- word_count

Contain following functions:
- test_null_input_error
- test_string_lenght_min
- test_string_lenght_max
- test_all_unique
- test_all_numeric
- test_unique_string_counts
- test_unique_mask_counts
- test_unique_word_counts
- test_word_stats
"""

# User defined modules
from utils.stringstatistics import StringStatistics
import pytest

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


def test_null_input_error():
    """
    Test whether ValueError will be raised in case of empty or only None
    input into StringStatistics().unique_count method.
    """

    test_null_input = [None, None, None]
    test_empty_input = []

    with pytest.raises(ValueError):
        StringStatistics().unique_count(test_null_input)
        StringStatistics().unique_count(test_empty_input)


def test_string_lenght_min():
    """
    Test lenght of string with minimum lenght will be returned correctly
    """

    # get stats from appropriate class
    dict_stats = StringStatistics().unique_count(test_data)["min_string_length"]

    # set the expected results
    correct_stats = 3

    # assert response
    assert dict_stats == correct_stats


def test_string_lenght_max():
    """
    Test lenght of string with maximum lenght will be returned correctly
    """

    # get stats from appropriate class
    dict_stats = StringStatistics().unique_count(test_data)["max_string_length"]

    # set the expected results
    correct_stats = 14

    # assert response
    assert dict_stats == correct_stats


def test_all_unique():
    """
    Test all_unique returns a correct value if unique_count method
    recieves a list of unique values.
    """

    test_unique_str = [
        'a',
        'b',
        'c',
    ]
    dict_stats = StringStatistics().unique_count(test_unique_str)["all_unique"]
    assert dict_stats is True


def test_all_numeric():
    """
    Test all_numeric returns a correct value if unique_count method
    recieves a list of strings containing only numbers.
    """

    test_numeric = [
        '11',
        '22',
        '333',
    ]
    dict_stats = StringStatistics().unique_count(test_numeric)["all_numeric"]
    assert dict_stats is True


def test_null_count_in_unique_count_method():
    """
    Test null values count in unique_count method
    """

    # get stats from appropriate class
    dict_stats = StringStatistics().unique_count(test_data)["null_count"]

    # set the expected results
    correct_stats = 2

    # assert response
    assert dict_stats == correct_stats


def test_unique_string_counts():
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


def test_unique_mask_counts():
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


def test_unique_word_counts():
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


def test_word_stats():
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
