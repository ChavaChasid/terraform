from dotenv import load_dotenv
import os

load_dotenv()


connection_string = os.getenv("CONNECTION_STRING")
time_period_for_check_last_fetch = os.getenv(
    "DESIRED_TIME_PERIOD_SINCE_LAST_RETRIEVAL_FOR_CHECK_LAST_FETCH"
)
time_period_for_check_used_capacity = os.getenv(
    "DESIRED_TIME_PERIOD_SINCE_LAST_RETRIEVAL_FOR_CHECK_USED_CAPACITY"
)
time_index_for_check_last_fetch = os.getenv("TIME_INDEX_FOR_CHECK_LAST_FETCH")
time_index_for_check_used_capacity = os.getenv("TIME_INDEX_FOR_CHECK_USED_CAPACITY")
freq_automation_test_type = os.getenv("FREQ_AUTOMATION_TEST_TYPE")
freq_automation_test_number = os.getenv("FREQ_AUTOMATION_TEST_NUMBER")
documentation_table = os.getenv("DOCUMENTATION_TABLE")
http_trigger_url = os.getenv("HTTP_TRIGGER_URL")
alerts_documentation = os.getenv("ALERTS_DOCUMENTATION")
documentation_storage_name = os.getenv("DOCUMENTATION_STORAGE_NAME")
managers_table = os.getenv("MANAGERS_TABLE")
connection_string_managers = os.getenv("CONNECTION_STRING_MANAGERS")
