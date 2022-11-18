import ckan.plugins as p
import ckan.plugins.toolkit as tk
from . import datastore_profiler

import json

class DatastoreProfilerPlugin(p.SingletonPlugin):

    def get_profile(self, id):
        # get profile information for all attributes except for _id
        raw = tk.get_action("datastore_search")(data_dict={"resource_id": id, "limit": 0})["fields"][1:]

        # put stringified json into actual dict
        for i in range(len(raw)):
            if isinstance(raw[i]["info"].get("profile", None), str):
                raw[i]["info"]["profile"] = json.loads( raw[i]["info"]["profile"] )
        
        # turn the output into a dict, with each attribute name as a key and each value as the attribute metadata
        output = {object["id"]:object for object in raw}
        return output

    

    # ==============================
    # IActions
    # ==============================
    # These are custom api endpoints
    # ex: hitting <ckan_url>/api/action/extract_info will trigger the api.extract_info function
    # These can also be used with tk.get_action("extract_info"), for example, in this CKAN extension code
    p.implements(p.IActions)

    def get_actions(self):
        return {
            "update_profile": datastore_profiler.update_profile,
            "datastore_create": datastore_profiler.datastore_create_hook,
        }

    # ==============================
    # IConfigurer
    # ITemplateHelpers
    # ==============================
    # This is what we use to make custom CKAN webpages

    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        tk.add_template_directory(config, 'profiler_templates')

    def get_helpers(self):
        return {
            "get_profile": self.get_profile,
        }