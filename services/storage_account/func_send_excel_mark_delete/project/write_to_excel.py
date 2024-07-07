from azure.storage.blob import BlobServiceClient
import pandas as pd
import os


def write_and_upload(connection_string, data):
    blob_file = "alert_file_storages.xlsx"
    container = "excel"
    write_excel_file(data, blob_file)
    upload_blob_file(connection_string, container, blob_file)


def write_excel_file(data, blob_file):
    df = pd.DataFrame(data)
    custom_header = [
        "Storage Account",
        "Alert Body",
        "Subscription Name",
        "Subscription Manager Email",
    ]
    df.to_excel(blob_file, index=False, header=custom_header)


def upload_blob_file(connection_string, container, blob_file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        container_client = blob_service_client.get_container_client(container=container)
        with open(os.path.join("./", blob_file), "rb") as data:
            container_client.upload_blob(name=blob_file, data=data, overwrite=True)
    except Exception:
        raise Exception("Failed to upload blob file")
