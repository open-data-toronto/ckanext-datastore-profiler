# datastore_profiler_utils.py - utilities for datastore_profiler.py

import re
import statistics
from datetime import datetime

def unique_count(input):
    # input list of strings
    # output list of dicts
    # each dict's key is a string from the input, and the number of times it appears as the value
    assert all(isinstance(x, str) for x in input if x), "Input to unique_count() must be all strings or null"

    # init output
    output = {}

    # build list of unique strings
    unique_values = list(set(input))

    # count how many times each string appears in input
    for unique_value in unique_values:
        output[unique_value] = len( [item for item in input if item == unique_value] )
    
    # add number of empty values to output
    if None in input:
        output["Value Empty/Null"] = len(input) - len([x for x in input if x]) 

    #return output
    return {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)}


def mask_count(input):
    # String mask creator
    # input a list of strings
    # returns a dicts - each key a "pattern" string, and each value how many times it occurs
    # the pattern has  L for letter, D for digit, and non alphanumerics as is
    assert all(isinstance(x, str) for x in input if x), "Input to mask_count() must be all strings or null"

    # init output
    output = {}

    # for each string
    for string in [x for x in input if x]:
        pattern = re.sub( '[a-zA-Z]', "L", string )
        pattern = re.sub( '[0-9]', "D", pattern )

        if pattern in output.keys():
            output[ pattern ] += 1
        else:
            output[ pattern ] = 1
    
    # add number of empty values to output
    if None in input:
        output["null_count"] = len(input) - len([x for x in input if x]) 

    #return output
    return {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)}


def numeric_count(input):
    # input list of ints and/or floats and/or nulls
    # outputs numeric stats on non-null values (and count of nulls)

    # make sure all inputs can be converted to integer
    assert all(isinstance(int(x), int) for x in input if x), "Input to min_max_med() must be all int, float or null"
    
    # remove nulls from working data
    working_data = [number for number in input if number]

    return {
        "min": min(working_data),
        "max": max(working_data),
        "median": statistics.median(working_data),
        "mean": statistics.mean(working_data),
        "null_count": len([item for item in input if item == None])
    }


def boolean_count(input):
    # input list of booleans and nulls
    # output count of True, False, and null values

    assert [value in [True, False, None] for value in input], "Input to boolean_count() can only be True, False, or Null"

    return {
        "true_count": len([val for val in input if val == True]),
        "false_count": len([val for val in input if val == False]),
        "null_count": len([val for val in input if val == None]),
    }


def timestamp_count(input):
    # input list of datetimes or nulls
    # output min date, max date, null counts
    # consider: number of times each year-month combo appears

    # make sure inputs are datetimes or nulls
    assert [isinstance(value, datetime) for value in input if value], "Input to timestamp_count can only be datetime or null"
    
    # remove nulls from working data
    working_data = [value for value in input if value]

    return {
        "min": min(working_data),
        "max": max(working_data),
        "null_count": len([value for value in input if value == None]),
    }
    

def word_count(input):
    # input list of strings
    # output list of dicts - each dict key is a "word" in any string, each value is how often it appears
    # a "word" is any string separated by spaces
    output = {}

    # make sure inputs are datetimes or nulls
    assert [isinstance(value, str) for value in input if value], "Input to word_count can only be string or null"

    # remove nulls from working data
    working_data = [value for value in input if value]

    # split each string by spaces, and make sure all the resulting "words" are in a single list
    working_words = " ".join(working_data).split(" ")

    # build list of unique strings, and of "words" to skip
    unique_values = list(set(working_words))
    words_to_skip = ["the", "this", "that", "a", "it"]

    # count how many times each string appears in input
    for unique_value in unique_values:
        if unique_value not in words_to_skip:
            output[unique_value] = len( [item for item in working_words if item == unique_value] )
    
    # add number of empty values to output
    if None in input:
        output["Value Empty/Null"] = len(input) - len([x for x in input if x]) 

    #return output sorted by count
    return {
        "word_counts": {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)},
        "min_word_count": min( [len(words.split(" ")) for words in working_data] ),
        "max_word_count": max( [len(words.split(" ")) for words in working_data] ),
        "min_string_length": min( [len(words) for words in working_data] ),
        "max_string_length": max( [len(words) for words in working_data] )
        }
    


if __name__ == "__main__":
    string_data = ["val2", "val3", "val4", "ccc-9", "d-1", "val-3", "val-3", "val1 val2 val3", "this is val1", "this is val2", None, None]
    num_data = [1,2,3,4,5,5.5, -5, 1213, 12.1231231231, 9, None]
    bool_data = [True, False, True, True, False, None, True]
    date_data = [datetime(2020,5,16), datetime.now(), None, datetime(1991, 6,14), None, None]

    print(unique_count(string_data))
    print(mask_count(string_data))
    print(numeric_count(num_data))
    print(boolean_count(bool_data))
    print(timestamp_count(date_data))
    print(word_count(string_data))
            
