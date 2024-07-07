from unittest.mock import patch, Mock
import pytest

from project.read_log_analytics import (
    get_max_times_log_each_storage,
    get_times_logs_per_table,
    get_times_logs,
    get_access_token,
    get_workspace_table,
    get_times,
    get_last_fetch_time_array,
)


class mock_adal:
    def AuthenticationContext(self, url):
        return mock_context()


class mock_context:
    def acquire_token_with_client_credentials(self, url, client_id, client_secret):
        return mock_token_response()


class mock_token_response:
    def get(self, access):
        return "token"


@patch("project.read_log_analytics.get_times", Mock(return_value="times"))
@patch("project.read_log_analytics.get_max_times_log_each_storage")
def test_get_last_fetch_time_array(get_max_times_log_each_storage):
    get_last_fetch_time_array()
    get_max_times_log_each_storage.assert_called_once_with("times")


@patch(
    "project.read_log_analytics.get_workspace_table",
    Mock(return_value="data_for_type_query"),
)
@patch("project.read_log_analytics.get_times_logs", Mock(return_value=["123", "456"]))
def test_get_times():
    assert get_times() == ["123", "456", "123", "456", "123", "456", "123", "456"]


def dumps(search_params):
    return search_params


@patch("project.read_log_analytics.workspace_id", "workspace_id")
@patch("project.read_log_analytics.get_access_token", Mock(return_value="access_token"))
@patch("project.read_log_analytics.json.dumps", dumps)
@patch("project.read_log_analytics.requests.post")
def test_get_workspace_table(post):
    get_workspace_table("type_query")
    filter_operations = (
        "GetBlob",
        "GetFile",
        "QueryEntities",
        "QueryTables",
        "PeekMessages",
        "GetMessages",
    )
    search_params = {
        "query": f"""Storagetype_queryLogs | project TimeGenerated, AccountName, Category, OperationName |  where Category == "StorageRead" and OperationName in {filter_operations} """,
        "timespan": "P7D",
    }
    post.assert_called_once_with(
        "https://api.loganalytics.io/v1/workspaces/workspace_id/search",
        headers={
            "Authorization": "Bearer access_token",
            "Content-Type": "application/json",
        },
        data=search_params,
    )


@patch("project.read_log_analytics.workspace_id", "workspace_id")
@patch("project.read_log_analytics.get_access_token", Mock(return_value="access_token"))
@patch("project.read_log_analytics.requests.post", Mock(side_effect=Exception()))
def test_get_workspace_table_failed_exception():
    with pytest.raises(Exception) as exception:
        get_workspace_table("type_query")
    assert "Failed to retrieve the data:" in str(exception.value)


@patch("project.read_log_analytics.tenant_id", "tenant_id")
@patch("project.read_log_analytics.client_id", "client_id")
@patch("project.read_log_analytics.client_secret", "client_secret")
@patch("project.read_log_analytics.adal", mock_adal())
def test_get_access_token():
    assert get_access_token() == "token"


@patch(
    "project.read_log_analytics.get_times_logs_per_table",
    Mock(side_effect=[[1, 2], [3, 4], [5, 6]]),
)
def test_get_times_logs():
    assert get_times_logs({"tables": [1, 2, 3]}) == [
        1,
        2,
        3,
        4,
        5,
        6,
    ]


def test_get_times_logs_per_table():
    assert get_times_logs_per_table({"rows": [[0, 1, 2], [0, 1, 2]]}) == [
        {"storage_name": 1, "time": 0},
        {"storage_name": 1, "time": 0},
    ]


@patch("project.read_log_analytics.sorted", Mock(return_value="sorted_data"))
@patch("project.read_log_analytics.itemgetter", Mock(return_value="storage_name"))
@patch(
    "project.read_log_analytics.groupby",
    Mock(
        return_value=[
            (
                "storage_name",
                {"storage_name": "storage1", "time": "2024-05-16T00:00:00.00000000Z"},
            ),
            (
                "storage_name",
                {"storage_name": "storage1", "time": "2024-06-16T00:00:00.00000000Z"},
            ),
            (
                "storage_name",
                {"storage_name": "storage2", "time": "2024-05-16T00:00:00.00000000Z"},
            ),
            (
                "storage_name",
                {"storage_name": "storage2", "time": "2024-06-16T00:00:00.00000000Z"},
            ),
        ]
    ),
)
@patch(
    "project.read_log_analytics.next",
    Mock(
        side_effect=[
            {"storage_name": "storage1", "time": "2024-05-16T00:00:00.00000000Z"},
            {"storage_name": "storage1", "time": "2024-06-16T00:00:00.00000000Z"},
            {"storage_name": "storage2", "time": "2024-05-16T00:00:00.00000000Z"},
            {"storage_name": "storage2", "time": "2024-06-16T00:00:00.00000000Z"},
        ]
    ),
)
def test_get_max_times_log_each_storage():
    assert get_max_times_log_each_storage(
        [
            {"storage_name": "storage1", "time": "2024-05-16T00:00:00.00000000Z"},
            {"storage_name": "storage1", "time": "2024-06-16T00:00:00.00000000Z"},
            {"storage_name": "storage2", "time": "2024-05-16T00:00:00.00000000Z"},
            {"storage_name": "storage2", "time": "2024-06-16T00:00:00.00000000Z"},
        ]
    ) == [
        {"storage_name": "storage1", "time": "2024-05-16T00:00:00.00000000Z"},
        {"storage_name": "storage1", "time": "2024-06-16T00:00:00.00000000Z"},
        {"storage_name": "storage2", "time": "2024-05-16T00:00:00.00000000Z"},
        {"storage_name": "storage2", "time": "2024-06-16T00:00:00.00000000Z"},
    ]
