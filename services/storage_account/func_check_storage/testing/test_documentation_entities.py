from datetime import date, timedelta
from unittest.mock import patch, Mock

from project.documentation_entities import (
    get_documentation_entities_by,
    calculate_start_and_end_dates,
    query_entities_between_two_dates,
    get_nearest_date_entity,
    get_first_entity,
    find_nearest_date_entity,
)


class mock_Table_client:
    def from_connection_string(self, con_str, table_name):
        return mock_connection()


class mock_connection:
    def query_entities(self, query_filter, select, parameters):
        return False


@patch("project.documentation_entities.TableClient", mock_Table_client())
@patch(
    "project.documentation_entities.calculate_start_and_end_dates",
    Mock(return_value=[date(2023, 11, 11), date(2023, 11, 11)]),
)
@patch(
    "project.documentation_entities.query_entities_between_two_dates",
    Mock(return_value="queried_entities"),
)
def test_get_documentation_entities_by():
    assert (
        get_documentation_entities_by(
            "storage_name", "x_time", "freq_test", "required_date"
        )
        == "queried_entities"
    )


@patch(
    "project.documentation_entities.return_seconds", Mock(side_effect=[7776000, 604800])
)
@patch(
    "project.documentation_entities.datetime",
    Mock(**{"timedelta.return_value": timedelta(seconds=7776000)}),
)
def test_calculate_start_and_end_dates_freq_test_less_and_equal_x_time_twice():
    start_date, end_date = calculate_start_and_end_dates(
        date(2023, 8, 8),
        {"type_of_time": "months", "number": 3},
        {"type_of_time": "weeks", "number": 1},
    )
    assert start_date == date(2023, 5, 10)
    assert end_date == date(2023, 11, 6)


@patch(
    "project.documentation_entities.return_seconds", Mock(side_effect=[604800, 7776000])
)
@patch(
    "project.documentation_entities.datetime",
    Mock(**{"timedelta.return_value": timedelta(seconds=604800)}),
)
def test_calculate_start_and_end_dates_freq_test_greater_than_x_time():
    start_date, end_date = calculate_start_and_end_dates(
        date(2023, 8, 8),
        {"type_of_time": "weeks", "number": 1},
        {"type_of_time": "months", "number": 3},
    )
    assert start_date == date(2023, 8, 1)
    assert end_date == date(2023, 8, 15)


@patch("project.documentation_entities.TableClient")
def test_query_entities_between_two_dates(TableClient):
    query_entities_between_two_dates(
        table_client=TableClient.from_connection_string("conn_stringAb1c2d34"),
        storage_name="storage name",
        start_date=date(2023, 7, 15),
        end_date=date(2023, 12, 12),
    )
    TableClient.from_connection_string().query_entities.assert_called_once_with(
        query_filter=f"storage_name eq @storage_name and test_date gt datetime'{date(2023,7,15)}T00:00:00Z' and test_date lt datetime'{date(2023,12,12)}T00:00:00Z'",
        select=["*"],
        parameters={"storage_name": "storage name"},
    )


@patch(
    "project.documentation_entities.get_first_entity",
    Mock(return_value={"test_date": "2023-08-15 00:00:00.000+00:00"}),
)
@patch(
    "project.documentation_entities.convert_to_date_type_mil_seconds",
    Mock(return_value=date(2023, 8, 15)),
)
@patch(
    "project.documentation_entities.calculate_diff_between_two_dates",
    Mock(return_value=57),
)
@patch("project.documentation_entities.find_nearest_date_entity")
def test_get_nearest_date_entity(find_nearest_date_entity):
    get_nearest_date_entity(
        [
            {"test_date": "2023-08-15 00:00:00.000+00:00"},
            {"test_date": "2023-09-11 00:00:00.000+00:00"},
            {"test_date": "2023-07-11 00:00:00.000+00:00"},
            {"test_date": "2023-08-11 00:00:00.000+00:00"},
        ],
        date(2023, 10, 11),
    )
    find_nearest_date_entity.assert_called_once_with(
        [
            {"test_date": "2023-08-15 00:00:00.000+00:00"},
            {"test_date": "2023-09-11 00:00:00.000+00:00"},
            {"test_date": "2023-07-11 00:00:00.000+00:00"},
            {"test_date": "2023-08-11 00:00:00.000+00:00"},
        ],
        date(2023, 10, 11),
        {"test_date": "2023-08-15 00:00:00.000+00:00"},
        date(2023, 8, 15),
        57,
    )


def test_get_first_entity():
    assert get_first_entity([{"entity": 1}, {"entity": 2}, {"entity": 3}]) == {
        "entity": 1
    }


def test_get_first_entity_empty():
    assert get_first_entity([]) is None


def test_find_nearest_date_entity():
    assert find_nearest_date_entity(
        queried_entities=[
            {"test_date": "2023-09-11 00:00:00.000+00:00"},
            {"test_date": "2023-07-11 00:00:00.000+00:00"},
            {"test_date": "2023-08-11 00:00:00.000+00:00"},
        ],
        required_date=date(2023, 10, 11),
        required_entity={"test_date": "2023-08-15 00:00:00.000+00:00"},
        nearest_date=date(2023, 8, 15),
        diff_days=57,
    ) == {"test_date": "2023-09-11 00:00:00.000+00:00"}
