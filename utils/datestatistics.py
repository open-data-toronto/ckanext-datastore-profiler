# datestatistics.py - class for summarizing lists of date and datetime/timestamp data

# Import python libraries
from dataclasses import dataclass
from datetime import datetime
from multiprocessing.sharedctypes import Value



@dataclass
class DateStatistics:
    '''
        This class is a Collection of methods that compute statistics on dates and timestamps (aka datetimes) 
    '''

    def date_or_timestamp(self, input):
        """
            determines whether input list contains dates or timestamps (aka datetimes)
        """
        results = []
        outputs = []
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

        for value in [str(val) for val in input if val]: # this list comp remove Null values from this
            # clean each value
            value = value.replace("/", "-")
            for format in format_dict.keys():
                # check each value against each possible date or datetime format     
                try:  
                    output = datetime.strptime(value, format)
                    outputs.append( output )

                    results.append( format_dict[format] )
                
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
        yearmonth_count = {}
        year_count = {}
        weekday_count = {}

        for date in working_data:
            # make working values for full dates, and the year-month of each date
            monthyear = date.strftime("%Y-%B")
            year = date.strftime("%Y") 
            weekday = date.strftime("%A")
            hour = date.strftime("%H")


            # then find counts for each unique date and year-month value
            if monthyear in yearmonth_count.keys():
                yearmonth_count[monthyear] += 1
            else:
                yearmonth_count[monthyear] = 1

            if year in year_count.keys():
                year_count[year] += 1
            else:
                year_count[year] = 1

            if weekday in weekday_count.keys():
                weekday_count[weekday] += 1
            else:
                weekday_count[weekday] = 1


        # extra analyses if input dates are timestamps
        hour_count = None # init this as None, in case it ought not be populated
        if scanned_input["data_type"] == "timestamp":
            hour_count = {}
            for timestamp in working_data:
                hour = timestamp.strftime("%H")
                if hour in hour_count.keys():
                    hour_count[hour] += 1
                else:
                    hour_count[hour] = 1

        return {
            "min": min(working_data).strftime("%Y-%m-%d"),
            "max": max(working_data).strftime("%Y-%m-%d"),
            "null_count": len([value for value in input if value == None]),
            "yearmonth_count": {k: v for k, v in sorted(yearmonth_count.items(), key=lambda item: item[1], reverse=True)},
            "year_count" : {k: v for k, v in sorted(year_count.items(), key=lambda item: item[1], reverse=True)}, 
            "weekday_count" : {k: v for k, v in sorted(weekday_count.items(), key=lambda item: item[1], reverse=True)}, 
            "hour_count": {k: v for k, v in sorted(hour_count.items(), key=lambda item: item[1], reverse=True)} if hour_count is not None else None,
        }
        
