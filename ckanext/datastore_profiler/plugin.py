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