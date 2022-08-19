import ckan.plugins as p
import ckan.plugins.toolkit as tk
from . import datastore_profiler

class DatastoreProfilerPlugin(p.SingletonPlugin):
    p.implements(p.IActions)

    # ==============================
    # IActions
    # ==============================
    # These are custom api endpoints
    # ex: hitting <ckan_url>/api/action/extract_info will trigger the api.extract_info function
    # These can also be used with tk.get_action("extract_info"), for example, in this CKAN extension code

    def get_actions(self):
        return {
            "update_profile": datastore_profiler.update_profile,
        }

    # ==============================
    # IConfigurer
    # ITemplateHelpers
    # ==============================
    # This is what we use to make custom CKAN webpages

    p.implements(p.IConfigurer)
    #p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        tk.add_template_directory(config, 'profiler_templates')

    #def get_helpers(self):
    #    return {
    #        "get_catalog": utils.get_catalog,
    #    }