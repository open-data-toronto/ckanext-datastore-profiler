# profiler-open-data-toronto
**What is this?**
This is a public repo for logic and documentation for Toronto's Open Data Profiler

**What is the Open Data Profiler**
Eventually, it will
1. Summarize each attribute in Toronto Open Data datastore resources
2. Assign classifications to each attribute
3. Present those on the Portal's API (and maybe frontend)

**How can I Contribute?**
- Reach out to opendata@toronto.ca
- Reach out on the Civic Tech Toronto Slack

## Descriptive Statitics for Integers and Floats:
- mean
- min
- max
- median
- count of distinct values

## Descriptive Statitics for Dates and Datetimes:
- earliest date
- latest date
- earliest time
- latest time
- count of distinct values for date
- count of distinct values for date month
- count of distinct values for date year
- count of distinct values for time

## Descriptive Statitics for Strings:
- count of distinct values
- count of distinct "words" (string separated by spaces, ignoring things like "this", "that", "a" etc
- min and max string length
- min and max word count per string
- count of distinct "masks" (where every letter of a string is turned into an "L" and every digit turned into a "D")

## Details about Test Driven Development (TDD)
- Test Driven Development is a great way to develop software. Especially when we have multiple combinations of datasets to test on. 
- I wrapped `datastore_profiler_utils.py/numeric_counts()` function as a method in `DataStatistics` class in `utils_profiler.py` file.
- I further, created a `test_utils_profiler.py` file that has collection of unittest to validate the profiler that we are building.  
- Here are the snippets on how to run the unittests from `utils` folder
```sh
python -m unittest -v 
```
- Output of the unittest will look like below
```sh
test_counts_of_values_in_list (test_utils_profiler.NumericStatisticsTestCase)
Testcase to check count of values in the list ... ok
test_max_value_from_list (test_utils_profiler.NumericStatisticsTestCase)
Testcase to check computation of max value from a list ... ok
test_mean_value_from_list (test_utils_profiler.NumericStatisticsTestCase)
Testcase to check computation of mean value from a list ... ok
test_median_value_from_list (test_utils_profiler.NumericStatisticsTestCase)       
Testcase to check computation of median value from a list ... ok
test_min_value_from_list (test_utils_profiler.NumericStatisticsTestCase)
Testcase to check computation of min value from a list ... ok
test_number_of_null_values_in_list (test_utils_profiler.NumericStatisticsTestCase)
Testcase to check no. of Null Values in the list ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.004s

OK
```
- My idea is that we write unittests not just at a data source level, but to validate our profiler when using multiple data sources. 

## Version Control & Best Coding Practices
- Steps to be followed to download updated code/documentation before start of any new development
```
# Create a new branch (branch_name: follows a convention that you are comfortable with) for new development 
git checkout -b branch_name origin/develop

# Rebase to make sure that we have updated code locally on the branch_name 
git pull --rebase origin develop
```

- Steps to be followed to upload any new developments related to code/documentation
```
# Push your developments from branch_name into develop branch on github repo.
git push origin branch_name
```

- Comment & commit as per the need.  
- Any development (small or big) should be subjected to peer-review i.e., sending Pull Request (PR) 
- E.g: Developer/Reviewers:
  - E.x-1: Mac develops code related to Statistics of Strings ---> Reviewer: Hareesh or Denis
  - E.x-2: Hareesh develops code related to Statistics of Date/Datetimes ---> Reviewer: Mackenzie or Denis
