import time
import rlink_client
from pprint import pprint
from rlink_client.apis.tags import default_api
# Defining the host is optional and defaults to https://aoe-api.reliclink.com
# See configuration.py for a list of all supported configuration parameters.
configuration = rlink_client.Configuration(
    host = "https://aoe-api.worldsedgelink.com"
)


profile_id = 76561197996386232

# Enter a context with an instance of the API client
with rlink_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = default_api.DefaultApi(api_client)
    title = 'age2'
    try:
        #query_params = {'title': title, 'profile_names': "[%22/steam/" + str(profile_id) + "%22]"}
        query_params = {
        'title': "age2",
        'profile_names': "[\"/steam/76561198342887481\"]",
        }
        api_response = api_instance.community_get_recent_match_history(query_params=query_params)
        api_instance.community_get_available_leaderboards({'title': "age2"})
        pprint(api_response)
        print(str(list(api_response.body['matchHistoryStats'])[0]['id']))
    except rlink_client.ApiException as e:
        print("Exception when calling DefaultApi->community_get_recent_match_history: %s\n" % e)