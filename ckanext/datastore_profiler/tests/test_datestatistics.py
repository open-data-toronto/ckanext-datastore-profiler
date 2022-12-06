# User defined modules
from utils.datestatistics import DateStatistics
from datetime import datetime
import pytest

test_dates = ["2020-06-12", "2020-06-12", "2001-06-12", "2020-06-21", "2020-06-26", "2020-06-26", "1987-11-12", "2020-11-12", "2020-11-12", "2020-11-12", "2020-12-12", None, None]
test_timestamps = ["2020-06-12T07:30:00", "2020-06-12T07:30:00", "2001-06-12T16:30:00", "2020-06-21T16:30:00", "2020-06-26T16:30:00", "2020-06-26T07:30:00", "1987-11-12T07:15:00", "2020-11-12T07:15:00", "2020-11-12T07:15:00", "2020-11-12T07:30:22", "2020-12-12T07:30:22", None, None]

date_dict_stats = DateStatistics().date_count(input = test_dates)
timestamp_dict_stats = DateStatistics().date_count(input = test_timestamps)

correct_min = '1987-11-12'
correct_max = '2020-12-12'
correct_null_count = 2
correct_yearmonth_count = {'2020-June': 5, '2020-November': 3, '2001-June': 1, '1987-November': 1, '2020-December': 1}
correct_year_count = {'2020': 9, '2001': 1, '1987': 1, }
correct_hour_count = {'07': 8, '16': 3}
correct_weekday_count = {'Friday': 4, 'Saturday': 1, 'Sunday': 1, 'Thursday': 4, 'Tuesday': 1}

# TO DO: write test cases for each of the above outputs

input_mix = ["2020-06-12 07:30:00", "2020-01-01"]

def test_date_format_error():
    with pytest.raises(TypeError):
        DateStatistics().date_or_timestamp(input = input_mix)

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

def test_year_count():
    """
        test case for DateStatistics class with input of strings representing dates and another input of strings representing  timestamps 
    """

    assert date_dict_stats["year_count"] == correct_year_count
    assert timestamp_dict_stats["year_count"] == correct_year_count

def test_weekday_count():
    """
        test case for DateStatistics class with input of strings representing dates and another input of strings representing  timestamps 
    """
    
    assert date_dict_stats["weekday_count"] == correct_weekday_count
    assert timestamp_dict_stats["weekday_count"] == correct_weekday_count

def test_hour_count():
    """
        test case for DateStatistics class with input of strings representing dates
    """

    assert timestamp_dict_stats["hour_count"] == correct_hour_count
