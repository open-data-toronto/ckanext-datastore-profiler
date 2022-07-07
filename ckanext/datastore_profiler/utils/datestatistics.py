# datestatistics.py - class for summarizing lists of date and datetime/timestamp data

# Import python libraries
from dataclasses import dataclass
from datetime import datetime
from multiprocessing.sharedctypes import Value

from collections import Counter


@dataclass
class DateStatistics:
    '''
        This class is a Collection of methods that compute statistics on dates and timestamps (aka datetimes) 
    '''

    def date_or_timestamp(self, input):
        """
            determines whether input list contains dates or timestamps (aka datetimes)
        """
        format_dict = {
            "%Y-%m-%dT%H:%M:%S.%f": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S.%f": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d": "%Y-%m-%d",
            "%d-%b-%Y": "%Y-%m-%d",
            "%d-%b-%y": "%Y-%m-%d",
            "%b-%d-%Y": "%Y-%m-%d",
            "%m-%d-%y": "%Y-%m-%d",
            "%m-%d-%Y": "%Y-%m-%d",
            "%d-%m-%y": "%Y-%m-%d",
            "%Y%m%d%H%M%S": "%Y-%m-%dT%H:%M:%S.%f",
            "%d%m%Y": "%Y-%m-%d",
            "%d%b%Y": "%Y-%m-%d",
        }

        for format in format_dict.keys():
            outputs = []
            results = []
            try:
                for value in [str(val).replace("/", "-") for val in input if val]: # this list comp remove Null values from this
                    # clean each value
                    #value = value.replace("/", "-")
                    
                    output = datetime.strptime(value, format)
                    outputs.append( output )

                    results.append( format_dict[format] )
                break
                
            except ValueError as e:
                pass
        

        
        if all( [result == "%Y-%m-%d" for result in results] ):
            return {"data_type": "date", "data": outputs}

        elif all( [result == "%Y-%m-%dT%H:%M:%S.%f" for result in results] ):
            return {"data_type": "timestamp" , "data": outputs}

        else:
            raise ValueError("Inputs to DateStatistics isn't all dates and isn't all datetimes/timestamps")

    def date_count(self, input):
        """
            Method to compute selected statistics on date data
    
        Args:
            input (list): List of strings that can be translated into date or timestamp values
                            - input list of strings that can be translated into date or timestamp values, or nulls
        Returns:
            output (dict): Dictionary with min, max, null_count, date_counts for dates, and distincs_counts for their month and year values
                            - outputs numeric stats on non-null values (and count of nulls)
        """

        # scan inputs to ensure theyre the right data type, and translate them accordingly
        scanned_input = self.date_or_timestamp(input)

        # make sure input contains only dates
        scanned_input["data_type"] in ["date", "timestamp"], "Inputs to date_count isn't all strings representing dates and isn't all strings representing datetimes/timestamps"

        # remove nulls from working data
        working_data = [value for value in scanned_input["data"] if value]

        # calculate distinct counts for month + years in input dates
        yearmonth_count = Counter([ date.strftime("%Y-%B") for date in working_data ])
        year_count = Counter([ date.strftime("%Y")  for date in working_data ])
        weekday_count = Counter([ date.strftime("%A") for date in working_data ])
        
        # extra analyses if input dates are timestamps
        hour_count = None # init this as None, in case it ought not be populated
        if scanned_input["data_type"] == "timestamp":
            hour_count = Counter([ date.strftime("%H") for date in working_data ])

        return {
            "min": min(working_data).strftime("%Y-%m-%d"),
            "max": max(working_data).strftime("%Y-%m-%d"),
            "null_count": len([value for value in input if value == None]),
            "yearmonth_count": {k: v for k, v in sorted(yearmonth_count.items(), key=lambda item: item[1], reverse=True)},
            "year_count" : {k: v for k, v in sorted(year_count.items(), key=lambda item: item[1], reverse=True)}, 
            "weekday_count" : {k: v for k, v in sorted(weekday_count.items(), key=lambda item: item[1], reverse=True)}, 
            "hour_count": {k: v for k, v in sorted(hour_count.items(), key=lambda item: item[1], reverse=True)} if hour_count is not None else None,
        }
        
