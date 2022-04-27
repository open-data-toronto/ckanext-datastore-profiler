# User defined modules
from utils.numericstatistics import NumericStatistics

test_data = [1,2,3,4,5,5.5, 5,5,5, -5, 1213, 12.1231231231, 9, None]
    
def test_min_value_from_list():
    """
        Testcase to check computation of min value from a list
    """
    # Compute stats from profiler
    dict_stats = NumericStatistics.numeric_count(test_data)

    # Assert response
    assert dict_stats.get('min') == -5

def test_max_value_from_list():
    """
        Testcase to check computation of max value from a list
    """
    # Compute stats from profiler
    dict_stats = NumericStatistics.numeric_count(test_data)

    # Assert response
    assert dict_stats.get('max') == 1213

def test_mean_value_from_list():
    """
        Testcase to check computation of mean value from a list
    """
    # Compute stats from profiler
    dict_stats = NumericStatistics.numeric_count(test_data)

    # Assert response
    assert dict_stats.get('mean') == 97.2787017787

def test_median_value_from_list():
    """
        Testcase to check computation of median value from a list
    """
    # Compute stats from profiler
    dict_stats = NumericStatistics.numeric_count(test_data)

    # Assert response
    assert dict_stats.get('median') == 5

def test_number_of_null_values_in_list():
    """
        Testcase to check no. of Null Values in the list
    """
    # Compute stats from profiler
    dict_stats = NumericStatistics.numeric_count(test_data)

    # Assert response
    assert dict_stats.get('null_count') == 1

def test_counts_of_values_in_list():
    """
        Testcase to check count of values in the list
    """
    # Compute stats from profiler
    dict_stats = NumericStatistics.numeric_count(test_data)

    # Expected output  
    dict_expected = {'1': 1, '2': 1, '3': 1, '4': 1, '5': 4, '5.5': 1, '-5': 1, '1213': 1, '12.1231231231': 1, '9': 1}

    # Assert response
    assert dict_stats.get('number_counts') == dict_expected