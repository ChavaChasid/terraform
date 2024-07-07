from http import HTTPStatus
import azure.functions as func
import json
import io

from project.managed_storages import get_storage_list
from config.config_variables import essential_tag


app = func.FunctionApp()


@app.function_name(name="HttpTrigger1")
@app.route(route="")
def func_get_storage_list_by_subscription(req: func.HttpRequest) -> func.HttpResponse:
    try:
        fix_bytes_value = req.get_body().replace(b"'", b'"')
        subscriptions_json = json.load(io.BytesIO(fix_bytes_value))
        storage_account_list = get_storage_list(subscriptions_json["subscription_id"])
        storage_accounts = []
        for storage_account in storage_account_list:
            storage_accounts.append(
                {
                    "name": storage_account.name,
                    "id": storage_account.id,
                    "tags": "true"
                    if storage_account.tags.get(essential_tag)
                    else "false",
                }
            )

        return func.HttpResponse(str(storage_accounts), status_code=HTTPStatus.OK)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
