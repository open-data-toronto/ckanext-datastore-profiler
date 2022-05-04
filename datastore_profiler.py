# datastore_profiler.py - for input package name's datastore resources, add profile object to each datastore field metadata
from fileinput import filename
import requests
import json
from utils import numericstatistics, datestatistics, stringstatistics
import pandas


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
        all_fields_metadata = self.get_datastore_resource_fields_metadata()
        for resource_id in all_fields_metadata.keys():
            # for each resource
            fields_metadata = all_fields_metadata[resource_id]
            
            # dump data into pandas dataframe
            df = pandas.read_csv( self.url + "datastore/dump/" + resource_id + "?format=csv", na_filter=False )
            
            # for each field, add appropriate profile to the metadata aobject
            for i in range(len(fields_metadata)):
                fieldname = fields_metadata[i]["id"]
                if fieldname == "_id": # we dont want to touch '_id' - we remove it later in this method
                    continue
                
                field_data = df[fieldname].tolist()

                if fields_metadata[i]["type"] in ["int", "int4", "float8"]:
                    fields_metadata[i]["info"]["profile"] = numericstatistics.NumericStatistics().numeric_count(field_data)
                elif fields_metadata[i]["type"] in ["date", "timestamp"]:
                    fields_metadata[i]["info"]["profile"] = datestatistics.DateStatistics().date_count(field_data)
                else:
                    fields_metadata[i]["info"]["profile"] = stringstatistics.StringStatistics().execute(field_data)

            # get rid of _id column - CKAN doesnt allow us to insert columns with that name
            for i in range(len(fields_metadata)):
                fieldname = fields_metadata[i]["id"]
                if fieldname == "_id":
                    fields_metadata.pop(i)
                    break
            
            # write edited resource metadata into ckan
            headers = {"Authorization": self.apikey}
            result = json.loads( self.session.post( self.url + "api/action/datastore_create", json={"resource_id": resource_id, "fields": fields_metadata, "force":True}, headers=headers ).text)
            assert result["success"], "Failed to update profiles for " + resource_id
            
    def visualize_datastore_resource(self, resource_id):
        """ 
            Run profiler on a data resource with resource_id
        """
        # dump data into pandas dataframe
        fields_json = pandas.read_json( self.url + "api/action/datastore_search?id=" + resource_id + "&limit=0")['result']['fields']
        
        # Flatten data
        df = pandas.json_normalize(fields_json, max_level=1)

        # Initialize dicts
        dict_numerics  = dict()
        dict_datetimes = dict()
        dict_strings   = dict()

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

                if (field_type in ["int", "int4", "float8"]):
                    dict_numerics[field_name] = field_profile         # append to dict_numerics 
                elif (field_type in ["date", "timestamp"]):
                    dict_datetimes[field_name] = field_profile        # append to dict_datetimes 
                else:
                    dict_strings[field_name] = field_profile          # append to dict_strings 

        # Convert dicts into dataframes
        df_numerics  = pandas.DataFrame(dict_numerics)
        df_datetimes = pandas.DataFrame(dict_datetimes)
        df_strings   = pandas.DataFrame(dict_strings)

        # Option-1: Save numerics stats as html table (for displaying on City's Page)
        df_numerics.T.to_html('html/table_numerics_stats.html')

        # Option-1: Save datetimes stats as html table (for displaying on City's Page)
        df_datetimes.T.to_html('html/table_datetimes_stats.html')

        # Option-1: Save strings stats as html table (for displaying on City's Page)
        df_strings.T.to_html('html/table_strings_stats.html')

        print('>> Completed - HTMLs')

        # # get rid of _id column - CKAN doesnt allow us to insert columns with that name
        # for i in range(len(fields_metadata)):
        #     fieldname = fields_metadata[i]["id"]
        #     if fieldname == "_id":
        #         fields_metadata.pop(i)
        #         break
        
        # # write edited resource metadata into ckan
        # headers = {"Authorization": self.apikey}
        # result = json.loads( self.session.post( self.url + "api/action/datastore_create", json={"resource_id": resource_id, "fields": fields_metadata, "force":True}, headers=headers ).text)
        # assert result["success"], "Failed to update profiles for " + resource_id
         


if __name__ == "__main__":
    # Data Resource Dump
    #Profiler("bodysafe", "https://ckanadmin0.intra.dev-toronto.ca/", "" ).profile_datastore_resources_dump()

    # Visualize Single Data Resource 
    resource_id = 'f9f84603-973c-43eb-bed0-a0ec26a2652b'
    Profiler("bodysafe", "https://ckanadmin0.intra.dev-toronto.ca/", "" ).visualize_datastore_resource(resource_id)