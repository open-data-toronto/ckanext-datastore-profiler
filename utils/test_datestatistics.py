# User defined modules
from utils.datestatistics import DateStatistics
from datetime import datetime

test_dates = ["2020-06-12", "2020-06-12", "2001-06-12", "2020-06-21", "2020-06-26", "2020-06-26", "1987-11-12", "2020-11-12", "2020-11-12", "2020-11-12", "2020-12-12", None, None]
test_timestamps = ["2020-06-12T07:30:00", "2020-06-12T07:30:00", "2001-06-12T16:30:00", "2020-06-21T16:30:00", "2020-06-26T16:30:00", "2020-06-26T07:30:00", "1987-11-12T07:15:00", "2020-11-12T07:15:00", "2020-11-12T07:15:00", "2020-11-12T07:30:22", "2020-12-12T07:30:22", None, None]

date_dict_stats = DateStatistics().date_count(input = test_dates)
timestamp_dict_stats = DateStatistics().date_count(input = test_timestamps)

correct_min = '1987-11-12'
correct_max = '2020-12-12'
correct_null_count = 2
correct_yearmonth_count = {'2020-06': 5, '2020-11': 3, '2001-06': 1, '1987-11': 1, '2020-12': 1}
correct_date_count = {'2020-11-12': 3, '2020-06-12': 2, '2020-06-26': 2, '2001-06-12': 1, '2020-06-21': 1, '1987-11-12': 1, '2020-12-12': 1}
correct_time_count = {'07:11': 4, '07:06': 3, '16:06': 3, '07:12': 1}

# TO DO: write test cases for each of the above outputs

def test_date_min():
    """
        test case for DateStatistics class with input of strings representing dates and another input of strings representing  timestamps 
    """

    assert date_dict_stats["min"] == correct_min
    assert timestamp_dict_stats["min"] == correct_min

def test_date_max():
    """
        test case for DateStatistics class with input of strings representing dates and another input of strings representing  timestamps 
    """

    assert date_dict_stats["max"] == correct_max
    assert timestamp_dict_stats["max"] == correct_max

def test_null_count():
    """
        test case for DateStatistics class with input of strings representing dates and another input of strings representing  timestamps 
    """

    assert date_dict_stats["null_count"] == correct_null_count
    assert timestamp_dict_stats["null_count"] == correct_null_count

def test_yearmonth_count():
    """
        test case for DateStatistics class with input of strings representing dates and another input of strings representing  timestamps 
    """

    assert date_dict_stats["yearmonth_count"] == correct_yearmonth_count
    assert timestamp_dict_stats["yearmonth_count"] == correct_yearmonth_count

def test_date_count():
    """
        test case for DateStatistics class with input of strings representing dates and another input of strings representing timestamps 
    """

    assert date_dict_stats["date_count"] == correct_date_count
    assert timestamp_dict_stats["date_count"] == correct_date_count

def test_time_count():
    """
        test case for DateStatistics class with input of strings representing dates
    """

    assert timestamp_dict_stats["time_count"] == correct_time_count
