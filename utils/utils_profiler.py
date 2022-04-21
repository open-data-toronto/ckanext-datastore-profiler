# Import python libraries
from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class DataStatistics:
    '''
        This class is a Collection of methods that compute statistics (based on input datatype) as required by OpenData 
    '''

    def numeric_count(input):
        """
            Method to compute selected statistics on numerical data
    
        Args:
            input (list): List of Numerical values
                            - input list of ints and/or floats and/or nulls
        Returns:
            output (dict): Dictionary with min, max, median, mean, null_count, number_counts information
                            - outputs numeric stats on non-null values (and count of nulls)
        """

        # make sure all inputs can be converted to integer
        assert all(isinstance(int(x), int) for x in input if x), "Input to min_max_med() must be all int, float or null"
        
        # remove nulls from working data
        working_data = [number for number in input if number]

        # calculate distinct counts that each number appears
        number_counts = {}
        for number in working_data:
            if str(number) in number_counts.keys():
                number_counts[str(number)] += 1
            else:
                number_counts[str(number)] = 1

        return {
            "min": np.min(working_data),
            "max": np.max(working_data),
            "median": np.median(working_data),
            "mean": np.mean(working_data),
            "null_count": len([item for item in input if item == None]),
            "number_counts": number_counts
        }

