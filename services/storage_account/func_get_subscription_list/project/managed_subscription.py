from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.data.tables import TableClient
import json
import pandas as pd

from config.config_variables import connection_string


def get_last_partition_key(table_name):
    try:
        table_client = TableClient.from_connection_string(connection_string, table_name)
        partitionKeys_table = convert_to_json(
            table_client.query_entities(
                query_filter="",
                select=["*"],
            )
        )
        if partitionKeys_table == {}:
            return -1
        table = [
            int(partition["PartitionKey"]) for partition in partitionKeys_table.values()
        ]
        return max(table)
    except Exception:
        raise Exception("Failed to get last partition key")


def convert_to_json(entities):
    return json.loads(pd.Series.to_json(pd.Series(entities)))


def get_subscription_list():
    subscription_client = create_subscription_client()
    try:
        sub_list = subscription_client.subscriptions.list()
        return sub_list
    except Exception:
        raise Exception("Failed to get subscription list")


def create_subscription_client():
    try:
        subscription_client = SubscriptionClient(credential=DefaultAzureCredential())
        return subscription_client
    except Exception:
        raise Exception("Failed to create subscription client")
