from project.date_functions import (
    convert_to_date_type_mil_seconds,
    get_date,
    calculate_diff_between_two_dates,
    convert_datetime_to_date,
)
from project.documentation_entities import get_documentation_entities_by
from config.config_variables import (
    time_index_for_check_last_fetch,
    time_period_for_check_last_fetch,
)


def check_last_fetch_is_early(
    storage_client, resource_group_name, storage_account_name, last_fetch_time
):
    result = {}
    freq_test = {
        "type_of_time": time_index_for_check_last_fetch,
        "number": int(time_period_for_check_last_fetch),
    }
    if last_fetch_time:
        result["last_fetch_time"] = str(last_fetch_time)[0:10]
        result["alert"] = False
    elif last_fetch_time := get_last_fetch_time_from_documentation(
        storage_account_name, freq_test
    ):
        result["last_fetch_time"] = last_fetch_time
        result["alert"] = False
    else:
        result["last_fetch_time"] = False
        result["alert"] = check_creation_date_is_early(
            storage_client, resource_group_name, storage_account_name, freq_test
        )

    return result


def get_last_fetch_time_from_documentation(storage_account_name, freq_test):
    x_time = {
        "type_of_time": "Day",
        "number": int(0),
    }
    required_date = get_date(x_time)

    query_entities = get_documentation_entities_by(
        storage_account_name, x_time, freq_test, required_date
    )
    try:
        required_entity = get_nearest_last_fetch_time_entity(query_entities)
        return required_entity
    except Exception:
        return False


def get_nearest_last_fetch_time_entity(query_entities):
    for entity in query_entities:
        if entity["last_storage_fetch_time"]:
            return entity["last_storage_fetch_time"]
    return False


def check_creation_date_is_early(
    storage_client, resource_group_name, storage_account_name, time_object
):
    date_creation_storage_account = get_creation_date(
        storage_client, resource_group_name, storage_account_name
    )

    return should_alert(time_object, date_creation_storage_account)


def get_creation_date(client, resource_group_name, storage_account_name):
    try:
        storage_account_properties = client.storage_accounts.get_properties(
            resource_group_name, storage_account_name
        )
        return convert_to_date_type_mil_seconds(
            str(storage_account_properties.creation_time)
        )
    except Exception:
        raise Exception("Failed to get creation date")


def should_alert(time_object, date):
    the_first_date_in_desired_period = get_date(time_object)
    difference_days = calculate_diff_between_two_dates(
        convert_datetime_to_date(the_first_date_in_desired_period),
        convert_datetime_to_date(date),
    )
    return difference_days >= 0
