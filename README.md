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
- Any `.py` file in the project that has `test` at the beginning or end of its filename will have any functions in it starting or ending with `test` will be run when `pytest` is run from `profiler-open-data-toronto` folder

- Output of successful tests will look like below
```sh
collected 10 items

utils\test_numericstatistics.py .....   [ 60%]
utils\test_stringstatistics.py ....     [100%]        

============ 10 passed in 1.09s ==============
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

## Using virtualenv and requirements.txt
To run this module locally, consider using `virtualenv`. To get started with `virtualenv`:

```sh
pip install virtualenv
cd path/to/profiler-open-data-toronto
virtualenv venv
```

This creates a `venv` folder, which you dont need to edit. This folder contains a portable python environment, where you can manage what `pip` installs separate from other environments on your machine or on other virtual environments.

To activate your virtual environment:
```sh
# on windows
.\venv\Scripts\activate.bat

# on *nix 
source venv/bin/activate

# to install the required modules
pip install -r requirements.txt
```

With the virtual environment active, any python scripts you run will have access to the needed modules in the correct versions


## Interactive visualization of Profiler outputs
This feature is hard-coded for POC v1.0. Change the `dtype` variable in **datastore_profiler.py** file and run the **datastore_profiler.py** to create interactive visual for specific datatype. 

- [x] Numerics
```py
# Change dtype variables in datastore_profiler.py
dtype = 'numerics'

# Run the file to create interactive visual
python datastore_profiler.py 
```
- [x] Datetimes 
```py
# Change dtype variables in datastore_profiler.py
dtype = 'datetimes'

# Run the file to create interactive visual
python datastore_profiler.py 
```
- [x] Strings - NOT IMPLEMENTED YET
