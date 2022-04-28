# stringstatistics.py - class(es) for summarizing lists of text/string data

# Import python libraries
import re

class StringStatistics:
    """
        This class is a Collection of methods that compute statistics for strings 
    """

    def unique_count(input):
        """
            Method to count unique strings
        Args:
            input (list): list of strings or nulls
        Returns:
            output (dict): output dict - each key is a string from the input, and the number of times it appears as the value                           
        """
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
        """
            Method to compute the count of masks for string data 
            Args:
                input (list): List of strings
            Returns:
                output (dict): each key a mask string, and each value how many times it occurs. Each mask has L for letter, D for digit, with each non-alphanumeric shown as is            
        """
        
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

    
    def word_count(input):
        
        """
                Method that splits each string by spaces and calculates statistics on each resulting "word"
            Args:
                input (list): of strings
            Returns:
                output (dict): each dict key is a "word" in any string, each value is how often it appears. A "word" is any string separated by spaces
        """
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

        # return output sorted by count
        return {
                "word_counts": {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)},
                "min_word_count": min( [len(words.split(" ")) for words in working_data] ),
                "max_word_count": max( [len(words.split(" ")) for words in working_data] ),
                "min_string_length": min( [len(words) for words in working_data] ),
                "max_string_length": max( [len(words) for words in working_data] )
            }