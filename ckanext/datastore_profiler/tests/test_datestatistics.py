"""
Test module for datestatistics module using pytest

Test date_count and date_or_timestamp methods under DateStatistics class.
The module contains the following functions:
- test_date_format_error
- test_date_min
- test_date_max
- test_null_count
- test_yearmonth_count
- test_year_count
- test_weekday_count
- test_hour_count
TEST M2
"""

import pytest
from utils.datestatistics import DateStatistics

# Define fixtures
@pytest.fixture
def test_dates():
    return [
        "2020-06-12",
        "2020-06-12",
        "2001-06-12",
        "2020-06-21",
        "2020-06-26",
        "2020-06-26",
        "1987-11-12",
        "2020-11-12",
        "2020-11-12",
        "2020-11-12",
        "2020-12-12",
        None,
        None,
        ]

@pytest.fixture
def test_timestamps():
    return [
        "2020-06-12T07:30:00",
        "2020-06-12T07:30:00",
        "2001-06-12T16:30:00",
        "2020-06-21T16:30:00",
        "2020-06-26T16:30:00",
        "2020-06-26T07:30:00",
        "1987-11-12T07:15:00",
        "2020-11-12T07:15:00",
        "2020-11-12T07:15:00",
        "2020-11-12T07:30:22",
        "2020-12-12T07:30:22",
        None,
        None,
        ]

@pytest.fixture
def input_mix():
    return ["2020-06-12 07:30:00", "2020-01-01"]

@pytest.fixture
def date_dict_stats(test_dates):
     date_dict_stats = DateStatistics().date_count(input=test_dates)
     return date_dict_stats

@pytest.fixture
def timestamp_dict_stats(test_timestamps):
    timestamp_dict_stats = DateStatistics().date_count(input=test_timestamps)
    return timestamp_dict_stats

#Define test functions
def test_date_format_error(input_mix):
    """
    Test whether TypeError will be raised in case of unsupported/incosistant
    input into the DateStatistics().date_or_timestamp method.
    """

    with pytest.raises(TypeError):
        DateStatistics().date_or_timestamp(input=input_mix)


def test_date_min(date_dict_stats, timestamp_dict_stats):
    """
    Test the expected min date/timestamp will be returend
    from DateStatistics().date_count method
    """

    correct_min = "1987-11-12"
    assert date_dict_stats["min"] == correct_min
    assert timestamp_dict_stats["min"] == correct_min


def test_date_max(date_dict_stats, timestamp_dict_stats):
    """
    Test the expected max date/timestamp will be returend
    from DateStatistics().date_count method
    """

    correct_max = "2020-12-12"
    assert date_dict_stats["max"] == correct_max
    assert timestamp_dict_stats["max"] == correct_max


def test_null_count(date_dict_stats, timestamp_dict_stats):
    """
    Test the expected null count in the inputted dates/timestamps will be
    returend from DateStatistics().date_count method
    """

    correct_null_count = 2
    assert date_dict_stats["null_count"] == correct_null_count
    assert timestamp_dict_stats["null_count"] == correct_null_count


def test_yearmonth_count(date_dict_stats, timestamp_dict_stats):
    """
    Test the expected year-month counts in the inputted dates/timestamps will
    be returend from DateStatistics().date_count method
    """

    correct_yearmonth_count = {
    "2020-June": 5,
    "2020-November": 3,
    "2001-June": 1,
    "1987-November": 1,
    "2020-December": 1,
    }
    assert date_dict_stats["yearmonth_count"] == correct_yearmonth_count
    assert timestamp_dict_stats["yearmonth_count"] == correct_yearmonth_count


def test_year_count(date_dict_stats, timestamp_dict_stats):
    """
    Test the expected year counts in the inputted dates/timestamps will
    be returend from DateStatistics().date_count method
    """

    correct_year_count = {
    "2020": 9,
    "2001": 1,
    "1987": 1,
    }
    assert date_dict_stats["year_count"] == correct_year_count
    assert timestamp_dict_stats["year_count"] == correct_year_count


def test_weekday_count(date_dict_stats, timestamp_dict_stats):
    """
    Test the expected weekday counts in the inputted dates/timestamps will
    be returend from DateStatistics().date_count method
    """

    correct_weekday_count = {
    "Friday": 4,
    "Saturday": 1,
    "Sunday": 1,
    "Thursday": 4,
    "Tuesday": 1,
    }
    assert date_dict_stats["weekday_count"] == correct_weekday_count
    assert timestamp_dict_stats["weekday_count"] == correct_weekday_count


def test_hour_count(timestamp_dict_stats):
    """
    Test the expected hour counts in the inputted dates/timestamps will
    be returend from DateStatistics().date_count method
    """

    correct_hour_count = {"07": 8, "16": 3}
    assert timestamp_dict_stats["hour_count"] == correct_hour_count
