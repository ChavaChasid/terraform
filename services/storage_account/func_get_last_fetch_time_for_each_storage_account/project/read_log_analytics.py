from itertools import groupby
from operator import itemgetter
import adal
import requests
import json

from config.config_variables import workspace_id, tenant_id, client_id, client_secret


def get_last_fetch_time_array():
    times = get_times()
    max_time_foreach_storage = get_max_times_log_each_storage(times)
    return max_time_foreach_storage


def get_times():
    storage_types = ["Table", "Queue", "Blob", "File"]
    times = []
    for type in storage_types:
        data_for_type_query = get_workspace_table(type)
        times_array = get_times_logs(data_for_type_query)
        times.extend(times_array)
    return times


def get_workspace_table(type_query):
    access_token = get_access_token()
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    filter_operations = (
        "GetBlob",
        "GetFile",
        "QueryEntities",
        "QueryTables",
        "PeekMessages",
        "GetMessages",
    )
    search_params = {
        "query": f"""Storage{type_query}Logs | project TimeGenerated, AccountName, Category, OperationName |  where Category == "StorageRead" and OperationName in {filter_operations} """,
        "timespan": "P7D",
    }
    url = f"https://api.loganalytics.io/v1/workspaces/{workspace_id}/search"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(search_params))
        print(response.json())
        return response.json()
    except requests.exceptions.HTTPError:
        return None
    except Exception as e:
        raise Exception(f"Failed to retrieve the data: {str(e)}")


def get_access_token():
    context = adal.AuthenticationContext(
        "https://login.microsoftonline.com/" + tenant_id
    )
    token_response = context.acquire_token_with_client_credentials(
        "https://api.loganalytics.io", client_id, client_secret
    )
    return token_response.get("accessToken")


def get_times_logs(data):
    arr = []
    for table in data["tables"]:
        arr.extend(get_times_logs_per_table(table))
    return arr


def get_times_logs_per_table(table):
    arr = []
    for i in range(len(table["rows"])):
        object_for_array = {
            "storage_name": table["rows"][i][1],
            "time": table["rows"][i][0],
        }
        arr.append(object_for_array)
    return arr


def get_max_times_log_each_storage(data):
    sorted_data = sorted(
        data, key=lambda x: (x["storage_name"], x["time"]), reverse=True
    )
    max_times_log_each_storage = [
        next(group)
        for key, group in groupby(sorted_data, key=itemgetter("storage_name"))
    ]
    return max_times_log_each_storage
