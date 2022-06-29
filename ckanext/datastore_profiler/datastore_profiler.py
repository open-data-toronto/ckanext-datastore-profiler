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

            print(fieldname)
            
            field_data = df[fieldname].tolist()

            if fields_metadata[i]["type"] in ["int", "int4", "float8"]:
                fields_metadata[i]["info"]["profile"] = NumericStatistics().numeric_count(field_data)
            elif fields_metadata[i]["type"] in ["date", "timestamp"]:
                fields_metadata[i]["info"]["profile"] = DateStatistics().date_count(field_data)
            else:
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
        print(result)
        
        # TODO: save and deploy this extension, then test it via an API call to DEV



class Profiler:
    def __init__(self, package_name, ckanaddress, apikey ):

        # init CKAN credentials
        self.url = ckanaddress
        self.apikey = apikey

        # init requests sessions to help avoid proxy errors
        self.session = requests.Session()
        self.session.trust_env = False

        # validate and init package name var
        assert package_name in json.loads( self.session.get( self.url + "api/action/package_list").text)["result"], "Input package name is not in " + self.url
        self.package_name = package_name


    def get_package_metadata(self):
        return json.loads( self.session.get( self.url + "api/action/package_show?id=" + self.package_name).text)["result"]

    def get_datastore_resource_fields_metadata(self):
        output = {}
        # for each datastore resource in self.package_name, return {resource_id: datastore fields metadata}
        for resource in self.get_package_metadata()["resources"]:
            if resource["datastore_active"] in [True]:
                # get attributes, length of datastore resource, and fields metadata
                datastore_resource_summary = json.loads( self.session.get( self.url + "api/action/datastore_search?limit=0&id=" + resource["id"]).text)["result"]
                output[ resource["id"] ] = datastore_resource_summary["fields"]

        return output

    def profile_datastore_resources_dump(self):
        """ 
            Loads all the OpenData data resources as a single dump file and runs the profiler on every data sources
        """
        resource_metadata = self.get_datastore_resource_fields_metadata()
        for resource_id in all_fields_metadata.keys():
            # for each resource
            fields_metadata = all_fields_metadata[resource_id]
            
            # dump data into pandas dataframe
            response = self.session.get( self.url + "datastore/dump/" + resource_id + "?format=csv" ).text
            df = pd.read_csv( io.StringIO(response), na_filter=False )
            
            # for each field, add appropriate profile to the metadata aobject
            for i in range(len(fields_metadata)):
                fieldname = fields_metadata[i]["id"]
                if fieldname == "_id": # we dont want to touch '_id' - we remove it later in this method
                    continue

                print(fieldname)
                
                field_data = df[fieldname].tolist()

                if fields_metadata[i]["type"] in ["int", "int4", "float8"]:
                    fields_metadata[i]["info"]["profile"] = NumericStatistics().numeric_count(field_data)
                elif fields_metadata[i]["type"] in ["date", "timestamp"]:
                    fields_metadata[i]["info"]["profile"] = DateStatistics().date_count(field_data)
                else:
                    fields_metadata[i]["info"]["profile"] = StringStatistics().execute(field_data)

            # get rid of _id column - CKAN doesnt allow us to insert columns with that name
            for i in range(len(fields_metadata)):
                fieldname = fields_metadata[i]["id"]
                if fieldname == "_id":
                    fields_metadata.pop(i)
                    break
            
            # write edited resource metadata into ckan
            headers = {"Authorization": self.apikey}
            result = json.loads( self.session.post( self.url + "api/action/datastore_create", json={"resource_id": resource_id, "fields": fields_metadata, "force":True}, headers=headers ).text)
            assert result["success"], "Failed to update profiles for " + resource_id + ":\n" + str(result)
            
    def visualize_datastore_resource(self, resource_id):
        """ 
            Run profiler on a data resource with resource_id
        """
        # dump data into pandas dataframe
        fields_json = pd.read_json( self.url + "api/action/datastore_search?id=" + resource_id + "&limit=0")['result']['fields']
        
        # Flatten data
        df = pd.json_normalize(fields_json, max_level=1)

        # Initialize dicts
        dict_numerics  = dict()
        dict_datetimes = dict()
        dict_strings   = dict()

        # Initialize emty keys list
        list_data_source_keys = list()

        # for each field, add appropriate profile to the metadata aobject
        for i in range(df.shape[0]):

            # Set fieldname
            field_name = df.loc[i, 'id']

            # Skip row if id = _id
            if field_name == "_id": # we dont want to touch '_id' 
                continue
            else:
                field_type = df.loc[i, 'type']
                field_profile = df.loc[i, 'info.profile']                
                print(i, field_name, field_type)

                # Append field_name to list of keys 
                list_data_source_keys.append(field_name)

                if (field_type in ["int", "int4", "float8"]):
                    dict_numerics[field_name] = field_profile         # append to dict_numerics 
                elif (field_type in ["date", "timestamp"]):
                    dict_datetimes[field_name] = field_profile        # append to dict_datetimes 
                else:
                    dict_strings[field_name] = field_profile          # append to dict_strings 

        # # Convert dicts into dataframes
        # df_numerics  = pd.DataFrame(dict_numerics)
        # df_numerics  = df_numerics.T
        # df_datetimes = pd.DataFrame(dict_datetimes)
        # df_datetimes = df_datetimes.T
        # df_strings   = pd.DataFrame(dict_strings)
        # df_strings   = df_strings.T

        # Display Stats as per MockUp
        plot_numeric_feature(dict_numerics, feature='inspID', lshow=True)
        #plot_timeseries_feature(dict_datetimes, feature='inspDate', lshow=True)
        #plot_string_feature(dict_strings, feature='enfrID', lshow=True)
        print('>> Completed - HTMLs')


if __name__ == "__main__":
    pass