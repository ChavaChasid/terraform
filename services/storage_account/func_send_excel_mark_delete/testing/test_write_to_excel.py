from unittest.mock import patch, Mock, mock_open

from project.write_to_excel import upload_blob_file, write_excel_file, write_and_upload


class mock_DataFrame:
    def DataFrame(self, data):
        return mock_to_excel()


class mock_to_excel:
    def to_excel(self, blob_file, index, header):
        return True


@patch("project.write_to_excel.write_excel_file", Mock(return_value=""))
@patch("project.write_to_excel.upload_blob_file")
def test_write_and_upload(upload_blob_file):
    write_and_upload("connection_string", "data")
    upload_blob_file.assert_called_once_with(
        "connection_string", "excel", "alert_file_storages.xlsx"
    )


@patch("project.write_to_excel.pd", mock_DataFrame())
def test_write_excel_file():
    assert not write_excel_file("data", "blob_file")


@patch("project.write_to_excel.os.path.join", Mock(return_value="./stam.txt"))
@patch("builtins.open", mock_open())
@patch("project.write_to_excel.BlobServiceClient")
def test_upload_blob_file(BlobServiceClient):
    upload_blob_file("connection_string", "container", "blob_file")
    BlobServiceClient.from_connection_string.assert_called_once_with(
        "connection_string"
    )
    BlobServiceClient.from_connection_string().get_container_client.assert_called_once_with(
        container="container"
    )
