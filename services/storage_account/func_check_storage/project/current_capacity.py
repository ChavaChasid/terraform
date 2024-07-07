import datetime
from project.connect_to_azure import (
    create_monitor_management_client,
    create_storage_management_client,
)


def get_used_capacity(subscription_id, resource_group_name, storage_account_name):
    storage_client = create_storage_management_client(subscription_id)
    storage_account = storage_client.storage_accounts.get_properties(
        resource_group_name, storage_account_name
    )
    monitor_client = create_monitor_management_client(subscription_id)
    metrics_data = get_metrics_list(storage_account, monitor_client)
    metric = return_first_row(metrics_data.value)
    time_series = return_first_row(metric.timeseries)
    if time_series.data[-1].total is None:
        return find_total_capacity(time_series.data) * (10**-6)
    return time_series.data[-1].total * (10**-6)


def get_metrics_list(storage_account, monitor_client):
    end_time = datetime.date.today()
    start_time = end_time - datetime.timedelta(days=1)
    time_span = f"{start_time}T00:00:00Z/{end_time}T00:00:00Z"
    try:
        metrics_data = monitor_client.metrics.list(
            storage_account.id,
            metricnames="UsedCapacity",
            timespan=time_span,
            interval="PT1H",
            aggregation="Total",
        )
        return metrics_data
    except Exception:
        raise Exception("Failed to get metrics list")


def return_first_row(obj):
    for metric in obj:
        return metric


def find_total_capacity(data_time_series):
    len_data_time_series = len(data_time_series)
    for i in reversed(range(len_data_time_series)):
        if data_time_series[i].total is not None:
            return data_time_series[i].total
    return 0
