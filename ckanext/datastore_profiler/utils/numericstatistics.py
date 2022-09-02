# numericstatistics.py - class for summarizing lists of numeric data

# Import python libraries
from dataclasses import dataclass
from collections import Counter


import statistics
import math


@dataclass
class NumericStatistics:
    '''
        This class is a Collection of methods that compute statistics (based on input datatype) as required by OpenData 
    '''

    def numeric_count(self, input):
        """
            Method to compute selected statistics on numerical data
    
        Args:
            input (list): List of Numerical values
                            - input list of ints and/or floats and/or nulls
        Returns:
            output (dict): Dictionary with min, max, median, mean, null_count, number_counts information
                            - outputs numeric stats on non-null values (and count of nulls)
        """


        # make sure all inputs can be converted to float
        input = [None if item == "None" else item for item in input]
        # number == number notation is to check for NaNs, since NaN does not equal itself
        assert all(isinstance(float(x), float) for x in input if x and x == x), "Input to numeric profiler must be all int, float or null"
        
        # remove nulls from working data
        working_data = [float(number) for number in input if number and number == number and number]

        if len(working_data) == 0:
            return {"all_null": True}

        # calculate distinct counts that each number appears
        number_counts = Counter(working_data)
        
        # if all numbers are unique, label the data as such
        all_unique = False
        if all( [value == 1 for value in number_counts.values()] ):
            all_unique = True

        # make sure this isnt all nulls
        null_count = len([item for item in input if item in [None, ''] or item != item])
        if null_count == len(input):
            return {"all_null": True}

        return {
            "min": min(working_data),
            "max": max(working_data),
            "median": statistics.median(working_data),
            "mean": statistics.mean(working_data),
            "null_count": null_count,
            "all_unique": all_unique,

        }

