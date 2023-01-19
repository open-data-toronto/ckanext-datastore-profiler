"""
Test module for numericstatistics module using pytest

Test numeric_count method under NumericStatistics class.
The module contains the following functions:
- test_invalid_input_error
- test_min_value
- test_max_value
- test_mean_value
- test_median_value
- test_number_of_null_values
"""

# Standard libraries

# Related third party libraries
import pytest

# Local application specific libraries
from utils.numericstatistics import NumericStatistics

# Define fixtures
@pytest.fixture
def test_data():
    return [
        1,
        2,
        3,
        4,
        5,
        5.5,
        5,
        5,
        5,
        -5,
        1213,
        12.1231231231,
        9,
        None,
        float("NaN"),
        ]

@pytest.fixture
def numeric_count_output(test_data):
    return NumericStatistics().numeric_count(test_data)

# Define test functions
def test_invalid_input_error():
    """
    Test raising ValueError when input is invalid (e.g. a string)
    """
    invalid_data = [1, "a"]
    with pytest.raises(ValueError):
        NumericStatistics().numeric_count(invalid_data)


def test_min_value(numeric_count_output):
    """
    Testcase to check computation of min value from a list
    """

    # Assert response
    assert numeric_count_output.get("min") == -5


def test_max_value(numeric_count_output):
    """
    Testcase to check computation of max value from a list
    """

    # Assert response
    assert numeric_count_output.get("max") == 1213


def test_mean_value(numeric_count_output):
    """
    Testcase to check computation of mean value from a list
    """

    # Assert response
    assert numeric_count_output.get("mean") == 97.2787017787


def test_median_value(numeric_count_output):
    """
    Testcase to check computation of median value from a list
    """

    # Assert response
    assert numeric_count_output.get("median") == 5


def test_number_of_null_values(numeric_count_output):
    """
    Testcase to check no. of Null Values in the list
    """

    # Assert response
    assert numeric_count_output.get("null_count") == 2
