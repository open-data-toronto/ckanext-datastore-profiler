# User defined modules
from utils.stringstatistics import StringStatistics

test_data =  ["val2", "val3", "val4", "ccc-9", "d-1", "val-3", "val-3", "val1 val2 val3", "this is val1", "this is val2", None, None]

def test_unique_string_counts_from_list():
    """
        Testcase to check computation of string counts from a list of strings
    """

    # get stats from appropriate class
    dict_stats = StringStatistics.unique_count(test_data)

    # set the expected results
    correct_stats = {'val-3': 2, None: 2, 'Value Empty/Null': 2, 'val3': 1, 'ccc-9': 1, 'this is val2': 1, 'd-1': 1, 'val1 val2 val3': 1, 'this is val1': 1, 'val4': 1, 'val2': 1}

    # assert response
    assert dict_stats == correct_stats

def test_unique_mask_counts_from_list():
    """
        Testcase to check computation of mask counts from a list of strings
    """

    # get stats from appropriate class
    dict_stats = StringStatistics.mask_count(test_data)

    # set the expected results
    correct_stats = {'LLLD': 3, 'LLL-D': 3, 'LLLL LL LLLD': 2, 'null_count': 2, 'L-D': 1, 'LLLD LLLD LLLD': 1}

    # assert response
    assert dict_stats == correct_stats

def test_unique_word_counts_from_list():
    """
        Testcase to check computation of word counts from a list of strings
    """

    # get stats from appropriate class
    dict_stats = StringStatistics.word_count(test_data).get("word_counts")

    # set the expected results
    correct_stats = {'val2': 3, 'val-3': 2, 'val3': 2, 'val1': 2, 'is': 2, 'Value Empty/Null': 2, 'ccc-9': 1, 'd-1': 1, 'val4': 1}

    # assert response
    assert dict_stats == correct_stats

def test_word_stats_from_list():
    """
        Testcase to check computation of word counts from a list of strings
    """

    # get stats from appropriate class
    dict_stats = StringStatistics.word_count(test_data)

    # set the expected results
    correct_stats = {'min_word_count': 1, 'max_word_count': 3, 'min_string_length': 3, 'max_string_length': 14}

    # assert responses
    assert dict_stats['min_word_count'] == correct_stats['min_word_count']
    assert dict_stats['max_word_count'] == correct_stats['max_word_count']
    assert dict_stats['min_string_length'] == correct_stats['min_string_length']
    assert dict_stats['max_string_length'] == correct_stats['max_string_length']