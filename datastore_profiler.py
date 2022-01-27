# datastore_profiler.py - for each datastore resource, create a summary of each of its attributes

import requests
import json
import datastore_profiler_utils

def check_assert(bool, out):
    if not bool:
        print(out)

# init environments to choose from for migration
url = "https://ckanadmin0.intra.prod-toronto.ca/"

# init output
output = []

# init requests sessions avoiding the use of a proxy
session = requests.Session()
session.trust_env = False

# get list of all package names from source and target, and sort them
package_names = json.loads( session.get( url + "api/action/package_list").text)["result"]

# for each package, check if its resources are datastore
for package_name in ["bodysafe"]:#package_names:
    package = json.loads( session.get( url + "api/action/package_show?id=" + package_name).text)["result"]
    # if this package has any datastore resources, look them up in detail
    for resource in package["resources"]:
        if resource["datastore_active"]:
            # get attributes, length of datastore resource
            datastore_resource_summary = json.loads( session.get( url + "api/action/datastore_search?limit=0&id=" + resource["id"]).text)["result"]
            data = {field["id"]: {"type": field["type"], "data": [] } for field in datastore_resource_summary["fields"] }
            # logic for smaller datastore resources
            if datastore_resource_summary["total"] < 32000:
                datastore_resource = json.loads( session.get( url + "api/action/datastore_search?limit=32000&id=" + resource["id"]).text)["result"]
                # for each record, stick into the "data" object
                for object in datastore_resource["records"]:
                    for field in list(object.keys()):
                        data[ field ]["data"].append( object[field] )


            # TODO: chunking logic for larger datastore resources
    
            # once data is put in to the data object, let's put it through our utils
            for field in datastore_resource_summary["fields"]:

                # for strings, we'll run string analyses
                print(field["id"])
                print(data[field["id"]]["type"])

                if data[field["id"]]["type"] == "text":
                    print(datastore_profiler_utils.mask_count(data[field["id"]]["data"]))
                    print(datastore_profiler_utils.unique_count(data[field["id"]]["data"]))

                if data[field["id"]]["type"] in ["int", "int4", "float", "float8"]:
                    print(datastore_profiler_utils.numeric_count(data[field["id"]]["data"]))

                if data[field["id"]]["type"] == "timestamp":
                    print( datastore_profiler_utils.timestamp_count(data[field["id"]]["data"]) )
            
            