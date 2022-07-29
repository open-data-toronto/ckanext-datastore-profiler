# numericstatistics.py - class for summarizing lists of numeric data

# Import python libraries
from dataclasses import dataclass

import statistics


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
        assert all(isinstance(float(x), float) for x in input if x), "Input to min_max_med() must be all int, float or null"
        
        # remove nulls from working data
        working_data = [float(number) for number in input if number]

        # calculate distinct counts that each number appears
        number_counts = {}
        for number in working_data:
            if str(number) in number_counts.keys():
                number_counts[str(number)] += 1
            else:
                number_counts[str(number)] = 1

        return {
            "min": min(working_data),
            "max": max(working_data),
            "median": statistics.median(working_data),
            "mean": statistics.mean(working_data),
            "null_count": len([item for item in input if item == None]),
            #"number_counts": number_counts
        }

