"""
Summarize a list/column of text/string data

This module contains the following class:
- StringStatistics

This module contains the following functions and methods:
- unique_count
- mask_count
- word_count
- geometry_stats
- execute
"""

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
            output (dict): output dict - each key is a string from the input,
            and the number of times it appears as the value
        """

        if not input or all(item is None for item in input):
            raise ValueError("The input is empty or only contains None values")

        # count how many times each string appears in input
        output = Counter(input)

        # if all strings are unique, label the data as such
        all_unique = False
        if all([value == 1 for value in output.values()]):
            all_unique = True

        # if all strings are numeric, label the data as such
        all_numeric = False
        if all([item.isdigit() for item in input if item]):
            all_numeric = True

        # add number of empty values to output
        if None in input:
            output["Value Empty/Null"] = len([x for x in input if x is None])

        # Calc lenght of strings
        input_lengths = [len(item) for item in input if item]

        # return output
        return {
            "min_string_length": min(input_lengths),
            "max_string_length": max(input_lengths),
            "counts": {
                k: v
                for k, v in sorted(
                    output.items(), key=lambda item: item[1], reverse=True
                )
            },
            "all_unique": all_unique,
            "all_numeric": all_numeric,
            "null_count": output["Value Empty/Null"],
        }

    def mask_count(self, input):
        """
        Method to compute the count of masks for string data
        Args:
            input (list): List of strings
        Returns:
            output (dict): each key a mask string, and each value how many
            times it occurs. Each mask has L for letter, D for digit, with
            each non-alphanumeric shown as is
        """

        # init output
        output = {}

        # for each string, create masks by replacing letters with "L" and
        # digits with "D", then count each mask
        masks = [
            re.sub("[0-9]", "D", re.sub("[a-zA-Z]", "L", str(x))) for x in input if x
        ]
        output = Counter(masks)

        # add number of empty values to output
        if None in input:
            output["null_count"] = len([x for x in input if x is None])

        return {
            "counts": {
                k: v
                for k, v in sorted(
                    output.items(), key=lambda item: item[1], reverse=True
                )
            }
        }

    def word_count(self, input):

        """
            Method that splits each string by spaces and calculates statistics
            on each resulting "word"
        Args:
            input (list): of strings
        Returns:
            output (dict): each dict key is a "word" in any string, each value
            is how often it appears. A "word" is any string separated by spaces
        """
        output = {}

        # remove nulls from working data
        working_data = [str(value) for value in input if value]

        # split each string by spaces, and make sure all the resulting "words"
        # are in a single list
        working_words = " ".join(working_data).split(" ")

        # build list of unique strings, and of "words" to skip
        output = Counter(working_words)
        stop_words = [
            "i",
            "me",
            "my",
            "myself",
            "we",
            "our",
            "ours",
            "ourselves",
            "you",
            "you're",
            "you've",
            "you'll",
            "you'd",
            "your",
            "yours",
            "yourself",
            "yourselves",
            "he",
            "him",
            "his",
            "himself",
            "she",
            "she's",
            "her",
            "hers",
            "herself",
            "it",
            "it's",
            "its",
            "itself",
            "they",
            "them",
            "their",
            "theirs",
            "themselves",
            "what",
            "which",
            "who",
            "whom",
            "this",
            "that",
            "that'll",
            "these",
            "those",
            "am",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "having",
            "do",
            "does",
            "did",
            "doing",
            "a",
            "an",
            "the",
            "and",
            "but",
            "if",
            "or",
            "because",
            "as",
            "until",
            "while",
            "of",
            "at",
            "by",
            "for",
            "with",
            "about",
            "against",
            "between",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "to",
            "from",
            "up",
            "down",
            "in",
            "out",
            "on",
            "off",
            "over",
            "under",
            "again",
            "further",
            "then",
            "once",
            "here",
            "there",
            "when",
            "where",
            "why",
            "how",
            "all",
            "any",
            "both",
            "each",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "s",
            "t",
            "can",
            "will",
            "just",
            "don",
            "don't",
            "should",
            "should've",
            "now",
            "d",
            "ll",
            "m",
            "o",
            "re",
            "ve",
            "y",
            "ain",
            "aren",
            "aren't",
            "couldn",
            "couldn't",
            "didn",
            "didn't",
            "doesn",
            "doesn't",
            "hadn",
            "hadn't",
            "hasn",
            "hasn't",
            "haven",
            "haven't",
            "isn",
            "isn't",
            "ma",
            "mightn",
            "mightn't",
            "mustn",
            "mustn't",
            "needn",
            "needn't",
            "shan",
            "shan't",
            "shouldn",
            "shouldn't",
            "wasn",
            "wasn't",
            "weren",
            "weren't",
            "won",
            "won't",
            "wouldn",
            "wouldn't",
        ]

        # count how many times each string appears in input
        for word in stop_words:
            if word in output.keys():
                output.pop(word)

        # add number of empty values to output
        if None in input:
            output["Value Empty/Null"] = len([x for x in input if x is None])

        # return output sorted by count
        return {
            # Return min No. of words in a given string
            "min_word_count": min([len(words.split(" ")) for words in working_data]),
            # Return max No. of words in a given string
            "max_word_count": max([len(words.split(" ")) for words in working_data]),
            # Count number of appearance of a word overall strings
            "word_counts": {
                k: v
                for k, v in sorted(
                    output.items(), key=lambda item: item[1], reverse=True
                )
            },
        }

    def geometry_stats(self, input):
        geometry_types = list(
            set([json.loads(object.replace('""', "'"))["type"] for object in input])
        )

        return {
            "geometry_types": geometry_types,
        }

    def execute(self, input):
        # we want to differentiate normal text from geometries
        # geometries are geojson objects with a "type" and "coordinates" key
        output = {
            "strings": {},
            "words": {},
            "masks": {},
        }

        try:
            # return geometry analytics, if this is a geometry string
            for item in input[:10]:
                parsed = json.loads(item.replace('""', "'"))
                assert (
                    "type" in parsed.keys() and "coordinates" in parsed.keys()
                ), "Missing geometry keys"

            return self.geometry_stats(input)

        except Exception:  # as e:

            output["strings"] = self.unique_count(input)

            if output["strings"].get("all_unique", None) or output.get(
                "all_numeric", None
            ):
                return output

            output["words"] = self.word_count(input)
            output["masks"] = self.mask_count(input)
            return output
