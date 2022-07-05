# stringstatistics.py - class(es) for summarizing lists of text/string data

# Import python libraries
import re
import json
from collections import Counter

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

        # count how many times each string appears in input    
        output = Counter(input)

        print("--------- unique value counts calculated")

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
        print("--------- Returning unique strings output ........")
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
        print("......... mask count start")
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
        print("......... mask count end!")
        return {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)}

    
    def word_count(self, input):
        
        """
                Method that splits each string by spaces and calculates statistics on each resulting "word"
            Args:
                input (list): of strings
            Returns:
                output (dict): each dict key is a "word" in any string, each value is how often it appears. A "word" is any string separated by spaces
        """
        print("--------- Word Count started")
        output = {}

        # remove nulls from working data
        working_data = [str(value) for value in input if value]

        # split each string by spaces, and make sure all the resulting "words" are in a single list
        working_words = " ".join(working_data).split(" ")

        print("---------- word count strings split into words")

        # build list of unique strings, and of "words" to skip
        unique_values = Counter(working_words)
        words_to_skip = ["the", "this", "that", "a", "it"]

        # count how many times each string appears in input
        for word in words_to_skip:
            if word in unique_values.keys():
                unique_values.pop( word )
        
        # add number of empty values to output
        if None in input:
            output["Value Empty/Null"] = len(input) - len([x for x in input if x]) 

        print("--------- Word Count ending...")

        # return output sorted by count
        return {
                "word_counts": {k: v for k, v in sorted(output.items(), key=lambda item: item[1], reverse=True)},
                "min_word_count": min( [len(words.split(" ")) for words in working_data] ),
                "max_word_count": max( [len(words.split(" ")) for words in working_data] ),
                "min_string_length": min( [len(words) for words in working_data] ),
                "max_string_length": max( [len(words) for words in working_data] )
            }
    
    def geometry_stats(self, input):
        geometry_types = list(set([ json.loads(object.replace('""', "'"))["type"] for object in input]))
        print(" -------------- ------------ successfully calculated geometry types")

        return {
            "geometry_types": geometry_types,
        }



    def execute(self, input):
        # we want to differentiate normal text from geometries 
        # geometries are geojson objects with a "type" and "coordinates" key
        try:
            
            for item in input[:10]:
                parsed = json.loads( item.replace('""', "'"))
                assert "type" in parsed.keys() and "coordinates" in parsed.keys(), "Missing geometry keys"
                    
            print("Geometry column identified")
            return self.geometry_stats(input)

        except Exception as e:
            print("============= Non Geometric column identified")
            output = self.unique_count(input)
            if output.get("all_unique", None) or output.get("all_numeric", None):
                print("-------------- ALL UNIQUE!")
                return output
            output["word_count"] = self.word_count(input)
            output["mask_count"] = self.mask_count(input)
            return output

