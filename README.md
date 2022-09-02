[![Tests](https://github.com/open-data-toronto/ckanext-datastore-profiler/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/open-data-toronto/ckanext-datastore-profiler/actions)

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


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | yes           |


## Installation

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


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
