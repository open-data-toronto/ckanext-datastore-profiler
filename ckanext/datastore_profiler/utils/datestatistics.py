"""
Summarize a list/column of dates/timestamps

This module contains the following class:
- DateStatistics

This module contains the following functions and methods:
- date_or_timestamp
- date_count
"""


from dataclasses import dataclass
from datetime import datetime
from collections import Counter


@dataclass
class DateStatistics:
    """
    This class computes statistics on dates and timestamps.

    Methods included:
    - date_or_timestamp
    - date_count
    """

    def date_or_timestamp(self, input):
        """
        Determines input contains dates or timestamps and turn them to datetime obj

        It maps inpputed dates/timestamps formats to standard/desired format.
        An exception will be raised if input format is not supported
        or all inputs are not following same formatting.

        Returns a dict containig date_type and translated dates/timestamps
        """

        # Mapping input format into the desired format
        format_dict = {
            "%Y-%m-%dT%H:%M:%S.%f": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S.%f": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S": "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d": "%Y-%m-%d",
            "%d-%b-%Y": "%Y-%m-%d",
            "%d-%b-%y": "%Y-%m-%d",
            "%b-%d-%Y": "%Y-%m-%d",
            "%b-%d-%y": "%Y-%m-%d",  # new
            "%m-%d-%y": "%Y-%m-%d",
            "%m-%d-%Y": "%Y-%m-%d",
            "%d-%m-%y": "%Y-%m-%d",
            "%Y%m%d%H%M%S": "%Y-%m-%dT%H:%M:%S.%f",
            "%d%m%Y": "%Y-%m-%d",
            "%d%b%Y": "%Y-%m-%d",
            # Less common formats
            "%d-%B-%Y": "%Y-%m-%d",
            "%d-%B-%y": "%Y-%m-%d",
            "%d%b%y": "%Y-%m-%d",
            "%d%B%y": "%Y-%m-%d",
            "%d%B%Y": "%Y-%m-%d",
            "%B-%d-%Y": "%Y-%m-%d",
            "%B-%d-%y": "%Y-%m-%d",
            "%y-%m-%d": "%Y-%m-%d",
            "%y-%b-%d": "%Y-%m-%d",
            "%y-%B-%d": "%Y-%m-%d",
        }

        # Transform the inputted date/timestamp strings into datetime obj
        # And store them and their final format
        for format in format_dict.keys():
            datetime_objects = []
            final_formats = []
            try:
                for value in [
                    val for val in input if val not in [None, "", "nan"]
                ]:  # this list comp remove Null values from this
                    # clean each value
                    value = str(value).replace("/", "-")

                    datetime_object = datetime.strptime(value, format)
                    datetime_objects.append(datetime_object)

                    final_formats.append(format_dict[format])
                break

            except ValueError:
                pass

        # Check the inputs are supported/cosistant
        # by checking final_formats list is still empty or not
        if not final_formats:
            raise TypeError("Unsupported/Inconsistant input format")

        # Return datetime_objects with their date_type tag
        if all([final_format == "%Y-%m-%d" for final_format in final_formats]):
            return {"data_type": "date", "data": datetime_objects}

        elif all(
            [final_format == "%Y-%m-%dT%H:%M:%S.%f" for final_format in final_formats]
        ):
            return {"data_type": "timestamp", "data": datetime_objects}

    def date_count(self, input):
        """
            Method to compute selected statistics on date data

        Args:
            input (list): List of strings that can be translated into date
            or timestamp values or nulls
        Returns:
            output (dict): Dictionary with min, max, null_count, date_counts
            for dates, and distincs_counts for their month and year values
                outputs numeric stats on non-null values (and count of nulls)
        """

        # Translate inputted date/timestamps strings into datetime object
        # A TypeEror will be returned if an unsupported/inconsisstant inputted
        scanned_input = self.date_or_timestamp(input)

        # remove nulls from working data
        working_data = [value for value in scanned_input["data"] if value]

        if len(working_data) == 0:
            return {"all_null": True}

        # Calculate distinct counts for month + years in input dates
        yearmonth_count = Counter([date.strftime("%Y-%B") for date in working_data])
        year_count = Counter([date.strftime("%Y") for date in working_data])
        weekday_count = Counter([date.strftime("%A") for date in working_data])

        # Extra analyses if input dates are timestamps
        hour_count = None  # init this as None, in case it ought not be populated
        if scanned_input["data_type"] == "timestamp":
            hour_count = Counter([date.strftime("%H") for date in working_data])

        return {
            "min": min(working_data).strftime("%Y-%m-%d"),
            "max": max(working_data).strftime("%Y-%m-%d"),
            "null_count": len([value for value in input if value is None]),
            "yearmonth_count": {
                k: v
                for k, v in sorted(
                    yearmonth_count.items(), key=lambda item: item[1], reverse=True
                )
            },
            "year_count": {
                k: v
                for k, v in sorted(
                    year_count.items(), key=lambda item: item[1], reverse=True
                )
            },
            "weekday_count": {
                k: v
                for k, v in sorted(
                    weekday_count.items(), key=lambda item: item[1], reverse=True
                )
            },
            "hour_count": {
                k: v
                for k, v in sorted(
                    hour_count.items(), key=lambda item: item[1], reverse=True
                )
            }
            if hour_count is not None
            else None,
        }
