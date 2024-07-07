from project.documentation_entities import (
    get_documentation_entities_by,
    get_nearest_date_entity,
)
from project.current_capacity import get_used_capacity
from project.date_functions import get_date
from config.config_variables import (
    freq_automation_test_type,
    freq_automation_test_number,
    time_index_for_check_used_capacity,
    time_period_for_check_used_capacity,
)


def used_capacity_comparison_test(resource_group_name, storage_name, subscription_id):
    current_used_capacity = get_used_capacity(
        subscription_id,
        resource_group_name,
        storage_name,
    )
    used_quantity_test_results = {
        "storage_name": storage_name,
        "resource_group": resource_group_name,
        "current_used_storage_capacity": current_used_capacity,
    }

    storage_information = get_storage_used_capacity_information(storage_name)
    if storage_information:
        used_quantity_test_results["alert"] = (
            current_used_capacity > storage_information["used_storage_capacity"]
        )
    else:
        used_quantity_test_results["alert"] = False
    return used_quantity_test_results


def get_storage_used_capacity_information(storage_name):
    x_time = {
        "type_of_time": freq_automation_test_type,
        "number": int(freq_automation_test_number),
    }
    freq_test = {
        "type_of_time": time_index_for_check_used_capacity,
        "number": int(time_period_for_check_used_capacity),
    }
    required_date = get_date(x_time)
    query_entities = get_documentation_entities_by(
        storage_name, x_time, freq_test, required_date
    )
    try:
        required_entity = get_nearest_date_entity(query_entities, required_date)
        return required_entity
    except Exception:
        return False
