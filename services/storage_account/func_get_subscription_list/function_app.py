from http import HTTPStatus
import azure.functions as func

from project.managed_subscription import (
    get_subscription_list,
    get_last_partition_key,
)
from config.config_variables import documentation_table


app = func.FunctionApp()


@app.function_name(name="HttpTrigger1")
@app.route(route="")
def func_get_subscription_list(req: func.HttpRequest) -> func.HttpResponse:
    try:
        subscription_list = get_subscription_list()
        partition_key = str(get_last_partition_key(documentation_table) + 1)
        subscriptions = []
        for subscription in subscription_list:
            subscriptions.append(
                {
                    "subscription_id": subscription.subscription_id,
                    "subscription_name": subscription.display_name,
                }
            )
        answer = {"subscriptions": subscriptions, "partition_key": str(partition_key)}

        return func.HttpResponse(str(answer), status_code=HTTPStatus.OK)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
