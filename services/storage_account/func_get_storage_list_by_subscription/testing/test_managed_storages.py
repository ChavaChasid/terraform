from unittest.mock import patch, Mock
import pytest

from project.managed_storages import create_storage_management_client, get_storage_list


@patch("project.managed_storages.create_storage_management_client")
def test_get_storage_list(create_storage_management_client):
    get_storage_list("a171324323")
    (
        create_storage_management_client.assert_called_once_with("a171324323"),
        "The function get_subscription_list doesn't send to create_subscription_client",
    )


def test_get_storage_list_return_exception():
    with pytest.raises(Exception) as exception:
        get_storage_list()
    assert "get_storage_list() missing 1 required positional argument: 'sub_id'" in str(
        exception.value
    )


@patch(
    "project.managed_storages.DefaultAzureCredential",
    Mock(return_value="default azure credential"),
)
@patch("project.managed_storages.StorageManagementClient")
def test_create_storage_management_client(StorageManagementClient):
    create_storage_management_client("123456-789")
    StorageManagementClient.assert_called_once_with(
        credential="default azure credential", subscription_id="123456-789"
    )


@patch(
    "project.managed_storages.create_storage_management_client",
    Mock(return_value="create_storage_management_client"),
)
def test_get_storage_list_raise_Exception():
    with pytest.raises(Exception, match="Failed to get storage list"):
        get_storage_list("sub_id")


@patch(
    "project.managed_storages.StorageManagementClient",
    Mock(side_effect=Exception("Exception")),
)
def test_create_storage_management_client_raise_exception():
    with pytest.raises(
        Exception, match="Failed to create storage account management client"
    ):
        create_storage_management_client("sub_id")
