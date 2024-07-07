from azure.mgmt.storage import StorageManagementClient
from azure.identity import DefaultAzureCredential


def get_storage_list(sub_id):
    storage_client = create_storage_management_client(sub_id)
    try:
        storage_accounts = storage_client.storage_accounts.list()
        return storage_accounts
    except Exception:
        raise Exception("Failed to get storage list")


def create_storage_management_client(sub_id):
    try:
        storage_client = StorageManagementClient(
            credential=DefaultAzureCredential(), subscription_id=sub_id
        )
        return storage_client
    except Exception:
        raise Exception("Failed to create storage account management client")
