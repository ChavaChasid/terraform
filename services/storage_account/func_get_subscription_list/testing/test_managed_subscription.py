from unittest.mock import patch, Mock
import pytest

from project.managed_subscription import (
    convert_to_json,
    get_last_partition_key,
    get_subscription_list,
    create_subscription_client,
)


@patch(
    "project.managed_subscription.DefaultAzureCredential",
    Mock(return_value="azure cli credential"),
)
@patch("project.managed_subscription.SubscriptionClient")
def test_create_subscription_client(SubscriptionClient):
    create_subscription_client()
    SubscriptionClient.assert_called_once_with(credential="azure cli credential")


@patch("project.managed_subscription.create_subscription_client")
def test_get_subscription_list(create_subscription_client):
    get_subscription_list()
    create_subscription_client.assert_called_once_with()


@patch("project.managed_subscription.connection_string", "123456-789456")
@patch(
    "project.managed_subscription.convert_to_json",
    Mock(
        return_value={
            "1": {"PartitionKey": "1"},
            "2": {"PartitionKey": "2"},
            "3": {"PartitionKey": "3"},
            "4": {"PartitionKey": "4"},
            "5": {"PartitionKey": "5"},
        }
    ),
)
@patch("project.managed_subscription.TableClient")
def test_get_last_partition_key_called_connection_string(TableClient):
    get_last_partition_key("table_name")
    TableClient.from_connection_string.assert_called_once_with(
        "123456-789456", "table_name"
    )


@patch("project.managed_subscription.connection_string", "123456-789456")
@patch(
    "project.managed_subscription.convert_to_json",
    Mock(
        return_value={
            "1": {"PartitionKey": "1"},
            "2": {"PartitionKey": "2"},
            "3": {"PartitionKey": "3"},
            "4": {"PartitionKey": "4"},
            "5": {"PartitionKey": "5"},
        }
    ),
)
@patch("project.managed_subscription.TableClient")
def test_get_last_partition_key_called_query_entities(TableClient):
    get_last_partition_key("table_name")
    TableClient.from_connection_string().query_entities.assert_called_once_with(
        query_filter="", select=["*"]
    )


@patch("project.managed_subscription.connection_string", "123456-789456")
@patch(
    "project.managed_subscription.convert_to_json",
    Mock(
        return_value={
            "1": {"PartitionKey": "1"},
            "2": {"PartitionKey": "2"},
            "3": {"PartitionKey": "3"},
            "4": {"PartitionKey": "4"},
            "5": {"PartitionKey": "5"},
        }
    ),
)
@patch("project.managed_subscription.TableClient")
def test_get_last_partition_key_return_5(TableClient):
    assert get_last_partition_key("table_name") == 5


@patch("project.managed_subscription.connection_string", "123456-789456")
@patch(
    "project.managed_subscription.convert_to_json",
    Mock(return_value={}),
)
@patch("project.managed_subscription.TableClient")
def test_get_last_partition_key_return_negative_one(TableClient):
    assert get_last_partition_key("table_name") == -1


@patch("project.managed_subscription.pd")
@patch("project.managed_subscription.json.loads", Mock(return_value="json"))
def test_convert_to_json_convert_entities(pd):
    assert convert_to_json("entities") == "json"


@patch("project.managed_subscription.connection_string", "connection_string")
@patch(
    "project.managed_subscription.convert_to_json",
    Mock(side_effect=Exception("Exception")),
)
@patch("project.managed_subscription.TableClient")
def test_get_last_partition_key_raise_Exception(TableClient):
    with pytest.raises(Exception, match="Failed to get last partition key"):
        get_last_partition_key("table_name")
