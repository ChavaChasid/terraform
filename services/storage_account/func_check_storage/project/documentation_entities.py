from azure.data.tables import TableClient
import datetime

from config.config_variables import (
    connection_string,
    documentation_table,
)
from project.date_functions import (
    calculate_diff_between_two_dates,
    convert_to_date_type_mil_seconds,
    return_seconds,
)


def get_documentation_entities_by(storage_name, x_time, freq_test, required_date):
    table_client = TableClient.from_connection_string(
        connection_string, documentation_table
    )
    start_date, end_date = calculate_start_and_end_dates(
        required_date, x_time, freq_test
    )
    queried_entities = query_entities_between_two_dates(
        table_client, storage_name, start_date, end_date
    )
    return queried_entities


def calculate_start_and_end_dates(required_date, x_time, freq_test):
    x_time_seconds = return_seconds(x_time)
    freq_test_seconds = return_seconds(freq_test)
    if freq_test_seconds <= (x_time_seconds * 2):
        start_date = required_date - datetime.timedelta(seconds=(x_time_seconds))
        end_date = required_date + datetime.timedelta(seconds=x_time_seconds)
    else:
        start_date = required_date - datetime.timedelta(seconds=freq_test_seconds)
        end_date = required_date + datetime.timedelta(seconds=freq_test_seconds)
    return start_date, end_date


def query_entities_between_two_dates(table_client, storage_name, start_date, end_date):
    parameters = {"storage_name": f"{storage_name}"}
    start_date = f"datetime'{start_date}T00:00:00Z'"
    end_date = f"datetime'{end_date}T00:00:00Z'"
    filter = f"storage_name eq @storage_name and test_date gt {start_date} and test_date lt {end_date}"
    try:
        queries_entities = table_client.query_entities(
            query_filter=filter,
            select=["*"],
            parameters=parameters,
        )
        return queries_entities
    except Exception:
        raise Exception("Failed to get queries entities")


def get_nearest_date_entity(queried_entities, required_date):
    required_entity = get_first_entity(queried_entities)
    nearest_date = convert_to_date_type_mil_seconds(str(required_entity["test_date"]))
    diff_days = calculate_diff_between_two_dates(required_date, nearest_date)
    required_entity = find_nearest_date_entity(
        queried_entities, required_date, required_entity, nearest_date, diff_days
    )
    return required_entity


def get_first_entity(queried_entities):
    for entity_chosen in queried_entities:
        return entity_chosen
    return


def find_nearest_date_entity(
    queried_entities, required_date, required_entity, nearest_date, diff_days
):
    for entity_chosen in queried_entities:
        nearest_date = convert_to_date_type_mil_seconds(str(entity_chosen["test_date"]))
        if abs(calculate_diff_between_two_dates(required_date, nearest_date)) < abs(
            diff_days
        ):
            diff_days = calculate_diff_between_two_dates(required_date, nearest_date)
            required_entity = entity_chosen
    return required_entity
