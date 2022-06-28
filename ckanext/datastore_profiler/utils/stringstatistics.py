# stringstatistics.py - class(es) for summarizing lists of text/string data

# Import python libraries
import re
import json

class StringStatistics:
    """
        This class is a Collection of methods that compute statistics for strings 
    """

    def unique_count(self, input):
        """
            Method to count unique strings
        Args:
            input (list): list of strings or nulls
        Returns:
            output (dict): output dict - each key is a string from the input, and the number of times it appears as the value                           
        """

        # init output
        output = {}

        # build list of unique strings
        unique_values = list(set(input))

        # count how many times each string appears in input
        for unique_value in unique_values:
            output[unique_value] = len( [item for item in input if item == unique_value] )

        # if all strings are unique, label the data as such
        if all( [value == 1 for value in output.values()] ):
            output = {"all_unique": True}

        # if all strings are numeric, label the data as such
        if all( [re.match(r'-?\d+\.?\d?', str(key)) for key in output.keys()] ):
            output["all_numeric"] = True
        
        # add number of empty values to output
        if None in input:
            output["Value Empty/Null"] = len(input) - len([x for x in input if x]) 

        #return output
        return {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)}


    def mask_count(self, input):
        """
            Method to compute the count of masks for string data 
            Args:
                input (list): List of strings
            Returns:
                output (dict): each key a mask string, and each value how many times it occurs. Each mask has L for letter, D for digit, with each non-alphanumeric shown as is            
        """
        
        # init output
        output = {}

        # for each string
        for string in [str(x) for x in input if x]:
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

    
    def word_count(self, input):
        
        """
                Method that splits each string by spaces and calculates statistics on each resulting "word"
            Args:
                input (list): of strings
            Returns:
                output (dict): each dict key is a "word" in any string, each value is how often it appears. A "word" is any string separated by spaces
        """
        output = {}

        # remove nulls from working data
        working_data = [str(value) for value in input if value]

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
    
    def geometry_stats(self, input):
        geometry_types = set([object["type"] for object in input])

        return {
            "geometry_types": geometry_types,
        }



    def execute(self, input):
        # we want to differentiate normal text from geometries 
        # geometries are geojson objects with a "type" and "coordinates" key
        try:
            
            for item in input:
                parsed = json.loads( item.replace('""', "'"))
                assert "type" in parsed.keys() and "coordinates" in parsed.keys(), "Missing geometry keys"
                    
            print("Geometry column identified")
            return self.geometry_stats(input)

        except Exception as e:

            output = self.word_count(input)
            output["unique_count"] = self.unique_count(input)
            output["mask_count"] = self.mask_count(input)
            return output

