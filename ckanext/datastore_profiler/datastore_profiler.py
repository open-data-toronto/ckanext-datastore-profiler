# datastore_profiler.py - for input package name's datastore resources, add profile object to each datastore field metadata
from fileinput import filename
from pydoc import source_synopsis
import requests
import json
import io
import csv
import re

from .utils.numericstatistics import NumericStatistics
from .utils.datestatistics import DateStatistics
from .utils.stringstatistics import StringStatistics
#from .utils.utils_plotting import plot_numeric_feature, plot_numerics, plot_pie_chart, plot_data_table, display_tables_in_tabs, display_strings_tables_for_ckan, plot_string_feature, plot_timeseries_feature

import ckan.plugins as p
import ckan.plugins.toolkit as tk


# need a function, with no_side_effect decorator, inputs are package id, resource id (optional) 
# create/updates profile of input resource/package
# does so on a queue, so API ... might not get response?

@tk.side_effect_free
def update_profile(context, data_dict):

    # make sure an authorized user is making this call
    assert context["auth_user_obj"], "This endpoint can be used by authorized accounts only"

    ### GET DATASTORE RESOURCE ATTRIBUTES FROM CKAN

    # init dict of resources to profile
    resource_ids = []
    resource_metadata = {}

    # if only package name is given, queue up all package's resources to profile
    if data_dict.get("package_id", None) and not data_dict.get("resource_id", None):
        package = tk.get_action("package_show")(context, {"id": data_dict["package_id"]})
        for resource in package["resources"]:
            if resource["datastore_active"] in [True, "True"]:
                resource_ids.append( resource["id"] )

    # if resource_id given, only queue that resource for profiling
    if data_dict.get("resource_id", None):
        resource = tk.get_action("resource_show")(context, {"id": data_dict["resource_id"]})
        if resource["datastore_active"] in [True, "True"]:
            resource_ids.append( resource["id"] )

    # assert that there are resources to profile
    #assert len(resource_ids) > 0, "No datastore resources in input"
    if len(resource_ids) == 0 :
        raise tk.ValidationError({ "Message": "No datastore resources found"})
        
    # get attributes, length of datastore resource, and fields 
    for resource_id in resource_ids:
        datastore_resource_summary =  tk.get_action("datastore_search")(context, {"limit":0, "id": resource_id})
        resource_metadata[ resource_id ] = datastore_resource_summary["fields"]

    ### CREATE PROFILE INPUT RESOURCES IN MEMORY

    for resource_id in resource_metadata.keys():
        # for each resource
        fields_metadata = resource_metadata[resource_id]
        
        # dump data into memory
        env = tk.config.get("ckan.site_url")
        dump = env + "/datastore/dump/" + resource_id
        data = []
        raw = requests.get(dump, stream=True)
        for line in raw.iter_lines():
            line = list(csv.reader(io.StringIO(line.decode("utf-8")), delimiter=","))
            data += line

        data = data[1:]


        
        # for each field, add appropriate profile to the metadata aobject
        for i in range(len(fields_metadata)):
            fieldname = fields_metadata[i]["id"]
            if fieldname == "_id": # we dont want to touch '_id' - we remove it later in this method
                continue

            # just get the data in this field
            field_data = [row[i] for row in data]

            if "info" not in fields_metadata[i].keys():
                fields_metadata[i]["info"] = {}

            # profiles are stored as stringified json objects
            if fields_metadata[i]["type"] in ["int", "int4", "float8"]:
                fields_metadata[i]["info"]["profile"] = json.dumps( NumericStatistics().numeric_count(field_data) )
            elif fields_metadata[i]["type"] in ["date", "timestamp"]:
                fields_metadata[i]["info"]["profile"] = json.dumps( DateStatistics().date_count(field_data) )
            else:
                fields_metadata[i]["info"]["profile"] = json.dumps( StringStatistics().execute(field_data) )

        # get rid of _id column - CKAN doesnt allow us to insert columns with that name
        for i in range(len(fields_metadata)):
            fieldname = fields_metadata[i]["id"]
            if fieldname == "_id":
                fields_metadata.pop(i)
                break

    ### ADD THAT PROFILE TO CKAN DATASTORE
        
        # write edited resource metadata into ckan
        result = tk.get_action("datastore_create")(context, {"resource_id": resource_id, "fields": fields_metadata, "force":True})

@tk.chained_action
def datastore_create_hook(original_datastore_create, context, data_dict):
    # triggers when datastore_create is called
    # it ensures that any tags on a newly updated datastore resource's attributes are 
    # also pushed to that resource's package's 'tags' object

    # make sure an authorized user is making this call
    print("------------ Checking Auth")
    tk.check_access("datastore_create", context, data_dict)
    assert context["auth_user_obj"], "This endpoint can be used by authorized accounts only"
    print("------------ Done Checking Auth")

    # run original datastore_create - we'll need its output to get package information
    datastore_create_output = original_datastore_create(context, data_dict)
    
    # collect resource attributes' tags
    tags = []
    for field in data_dict["fields"]:
        print(field["info"].get("tags", None))
        if field["info"].get("tags", None):
            tags.append(field["info"]["tags"])

    # make sure there is a vocabulary for attribute tags
    vocabulary = [vocabulary for vocabulary in tk.get_action("vocabulary_list")(context) if vocabulary["name"] == "attribute_tags"]
    # if attribute_tags isnt a vocabulary, make it and grab its ID
    if not vocabulary:
        vocabulary = tk.get_action("vocabulary_create")(context, {"name": "attribute_tags"})
    # if the vocabulary exists, unpack it from its enveloping array
    else:
        vocabulary = vocabulary[0]

    # get package info
    resource = tk.get_action("resource_show")(context, {"id": datastore_create_output["resource_id"]} )
    package = tk.get_action("package_show")(context, {"id": resource["package_id"]} )
    package_tags = [tag for tag in package["tags"] if tag["vocabulary_id"] == None ]


    # compile tags from each datastore resource that is NOT this datastore resource
    for resource in [ r for r in package["resources"] if r.get("datastore_active", None) in [True, "true", "True"] and r["id"] != datastore_create_output["resource_id"] ]:
        datastore_resource = tk.get_action("datastore_search")(context, {"id": resource["id"], "limit": 0})
        if field["info"].get("tags", None):
            print("Appending {} to tags".format(field["info"]["tags"]) )
            tags.append( field["info"]["tags"] )

    # if its a new tag, add the tag
    for tag in tags:
        # add tag and its association to attribute_tags vocabulary to CKAN
        if tag not in [tag["name"] for tag in vocabulary["tags"]]:
            tag_object = tk.get_action("tag_create")(context, {"name": tag, "vocabulary_id": vocabulary["id"]})
        # else grab a tag object if it already exists in a vocabulary
        else:
            tag_object = [t for t in vocabulary["tags"] if t["name"] == tag][0]

        # add package tags (which have no dictionary associated w them) to attribute tags (from this newly changed datastore resource and all others in the package)
        package_tags.append( tag_object )

    tk.get_action("package_patch")(context, {"id": package["name"], "tags": package_tags })
