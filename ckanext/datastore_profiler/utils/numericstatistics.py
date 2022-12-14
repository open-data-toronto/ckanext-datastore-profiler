"""
Summarize a list/column of numbers

This module contains the following class:
- NumericStatistics

This module contains the following functions and methods:
- numeric_count
"""

# Standard libraries
from collections import Counter
import statistics

# Related third party libraries

# Local application specific libraries
from dataclasses import dataclass


@dataclass
class NumericStatistics:
    """
    This class computes statistics on numbers.

    Methods included:
    - numeric_count
    """

    def numeric_count(self, input):
        """
            Method to compute selected statistics on numerical data

        Args:
            input (list): List of Numerical values
                            - input list of ints and/or floats and/or nulls
        Returns:
            output (dict): Dictionary with min, max, median, mean, null_count,
            number_counts information
                            - outputs numeric stats on non-null values (and
                            count of nulls)
        """

        # convert "None" stings to None object
        input = [None if item == "None" else item for item in input]

        # Check the inputs are valid. Allowed inputs are float, int, NaN, and None

        try:
            all(isinstance(float(x), float) for x in input if x and x == x)
        except ValueError:
            print("Input to numeric profiler must be all int, float, NaN, or null")

        # remove null and NaN from input
        working_data = [
            float(number) for number in input if number and number == number
        ]

        if len(working_data) == 0:
            return {"all_null": True}

        # calculate distinct counts that each number appears
        number_counts = Counter(working_data) 

        # if all numbers are unique, label the data as such
        all_unique = False
        if all([value == 1 for value in number_counts.values()]):
            all_unique = True

        # make sure this is not all nulls and NaN
        null_count = len([item for item in input if item in [None, ""] or item != item])
        if null_count == len(input):
            return {"all_null": True}

        return {
            "min": min(working_data),
            "max": max(working_data),
            "median": statistics.median(working_data),
            "mean": statistics.mean(working_data),
            "null_count": null_count,
            "all_unique": all_unique,
            "total_values_count": len(working_data)
        }
