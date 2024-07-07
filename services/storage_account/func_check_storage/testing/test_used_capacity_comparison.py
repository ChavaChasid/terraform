from unittest.mock import patch, Mock

from project.used_capacity_comparison import (
    used_capacity_comparison_test,
    get_storage_used_capacity_information,
)


@patch(
    "project.used_capacity_comparison.get_storage_used_capacity_information",
    Mock(
        return_value={
            "subscription_id": "a17",
            "resource_group": "resource_group",
            "storage_name": "storage_name",
            "used_storage_capacity": 30.5,
        }
    ),
)
@patch("project.used_capacity_comparison.get_used_capacity", Mock(return_value=20.5))
def test_used_capacity_comparison_test_return_object():
    used_capacity_comparison_test_object = used_capacity_comparison_test(
        "resource_group_name", "storage_name", "subscription_id"
    )
    assert used_capacity_comparison_test_object == {
        "storage_name": "storage_name",
        "resource_group": "resource_group_name",
        "current_used_storage_capacity": 20.5,
        "alert": False,
    }


@patch(
    "project.used_capacity_comparison.get_storage_used_capacity_information",
    Mock(return_value={}),
)
@patch("project.used_capacity_comparison.get_used_capacity", Mock(return_value=20.5))
def test_used_capacity_comparison_test_return_object_with_alert_False():
    used_capacity_comparison_test_object = used_capacity_comparison_test(
        "resource_group_name", "storage_name", "subscription_id"
    )
    assert used_capacity_comparison_test_object == {
        "storage_name": "storage_name",
        "resource_group": "resource_group_name",
        "current_used_storage_capacity": 20.5,
        "alert": False,
    }


@patch("project.used_capacity_comparison.time_index_for_check_used_capacity", "Day")
@patch("project.used_capacity_comparison.freq_automation_test_type", "Day")
@patch("project.used_capacity_comparison.freq_automation_test_number", "3")
@patch("project.used_capacity_comparison.time_period_for_check_used_capacity", "3")
@patch("project.used_capacity_comparison.get_date", Mock(return_value="12-05-2024"))
@patch("project.used_capacity_comparison.get_documentation_entities_by")
def test_get_storage_used_capacity_information_called_get_documentation_entities_by(
    get_documentation_entities_by,
):
    get_storage_used_capacity_information("storage_name")
    get_documentation_entities_by.assert_called_once_with(
        "storage_name",
        {
            "type_of_time": "Day",
            "number": 3,
        },
        {
            "type_of_time": "Day",
            "number": 3,
        },
        "12-05-2024",
    )


@patch("project.used_capacity_comparison.time_index_for_check_used_capacity", "Day")
@patch("project.used_capacity_comparison.freq_automation_test_type", "Day")
@patch("project.used_capacity_comparison.freq_automation_test_number", "3")
@patch("project.used_capacity_comparison.time_period_for_check_used_capacity", "3")
@patch("project.used_capacity_comparison.get_date", Mock(return_value="12-05-2024"))
@patch(
    "project.used_capacity_comparison.get_documentation_entities_by",
    Mock(return_value=[{"aaa"}, {"bbb"}]),
)
@patch(
    "project.used_capacity_comparison.get_nearest_date_entity",
    Mock(side_effect=Exception()),
)
def test_get_storage_used_capacity_information_raise_execption():
    assert not get_storage_used_capacity_information("storage_name")
