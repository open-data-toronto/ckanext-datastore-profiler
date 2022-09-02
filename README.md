[![Tests](https://github.com/open-data-toronto/ckanext-datastore-profiler/workflows/Tests/badge.svg?branch=main)](https://github.com/open-data-toronto/ckanext-datastore-profiler/actions)

# ckanext-datastore-profiler
**What is this?**
This is a public repo for logic and documentation for Toronto's Open Data Profiler

**What is the Profiler**
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


## Requirements

**TODO:** For example, you might want to mention here which versions of CKAN this
extension works with.

If your extension works across different versions you can add the following table:

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | yes           |


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-datastore-profiler:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/open-data-toronto/ckanext-datastore-profiler.git
    cd ckanext-datastore-profiler
    pip install -e .
	pip install -r requirements.txt

3. Add `datastore-profiler` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.datastore_profiler.some_setting = some_default_value


## Developer installation

To install ckanext-datastore-profiler for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/open-data-toronto/ckanext-datastore-profiler.git
    cd ckanext-datastore-profiler
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-datastore-profiler

If ckanext-datastore-profiler should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
