# datastore_profiler.py - for input package name's datastore resources, add profile object to each datastore field metadata
from fileinput import filename
from pydoc import source_synopsis
import requests
import json
import pandas as pd
import io

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
    assert len(resource_ids) > 0, "The inputs to the datastore profilers ({}) were not associated with any datastore resources".format( data_dict["package_id"] + " " + data_dict["resource_id"] )
        
    # get attributes, length of datastore resource, and fields 
    for resource_id in resource_ids:
        datastore_resource_summary =  tk.get_action("datastore_search")(context, {"limit":0, "id": resource_id})
        resource_metadata[ resource_id ] = datastore_resource_summary["fields"]

    

    ### CREATE PROFILE INPUT RESOURCES IN MEMORY

    for resource_id in resource_metadata.keys():
        # for each resource
        fields_metadata = resource_metadata[resource_id]
        
        # dump data into pandas dataframe
        env = tk.config.get("ckan.site_url")
        dump = env + "/datastore/dump/" + resource_id
        df = pd.read_csv( dump )
        
        # for each field, add appropriate profile to the metadata aobject
        for i in range(len(fields_metadata)):
            fieldname = fields_metadata[i]["id"]
            if fieldname == "_id": # we dont want to touch '_id' - we remove it later in this method
                continue

            print("================================ FIELD:")
            print(fieldname)
            
            field_data = df[fieldname].tolist()

            if "info" not in fields_metadata[i].keys():
                fields_metadata[i]["info"] = {}

            if fields_metadata[i]["type"] in ["int", "int4", "float8"]:
                print("------- NUMERIC")
                fields_metadata[i]["info"]["profile"] = NumericStatistics().numeric_count(field_data)
            elif fields_metadata[i]["type"] in ["date", "timestamp"]:
                print("------- TIMESTAMP")
                fields_metadata[i]["info"]["profile"] = DateStatistics().date_count(field_data)
            else:
                print("------- STRING")
                fields_metadata[i]["info"]["profile"] = StringStatistics().execute(field_data)

        # get rid of _id column - CKAN doesnt allow us to insert columns with that name
        for i in range(len(fields_metadata)):
            fieldname = fields_metadata[i]["id"]
            if fieldname == "_id":
                fields_metadata.pop(i)
                break

    ### ADD THAT PROFILE TO CKAN DATASTORE
        
        # write edited resource metadata into ckan
        result = tk.get_action("datastore_create")(context, {"resource_id": resource_id, "fields": fields_metadata, "force":True})