from http import HTTPStatus
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
import requests
import json

from config.config_variables import (
    documentation_table,
    main_manager,
    http_trigger_url,
    excel_connection_string,
)
from project.managed_deleted_storages import (
    deleted_storages,
)
from project.write_to_excel import write_and_upload


app = func.FunctionApp()


@app.function_name(name="HttpTrigger1")
@app.route(route="")
def func_send_excel_mark_delete(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_body()
        my_json = body.decode("utf8").replace("'", '"')
        data = json.loads(my_json)
        alerts_to_excel = data["alerts_to_excel"]
        partition_key = data["partition_key"]
        all_storages = data["all_storages"]
        all_storages = [storage.strip() for storage in all_storages]
        if len(alerts_to_excel):
            write_and_upload(excel_connection_string, alerts_to_excel)
            requests.post(
                http_trigger_url,
                json={
                    "recipient_email": main_manager,
                    "subject": "Summary Alerts For Storage Accounts",
                    "body": "summary file",
                    "excel": "alert_file_storages.xlsx",
                },
            )
        deleted_storages(documentation_table, int(partition_key) - 1, all_storages)
        return func.HttpResponse("success - end logic app", status_code=HTTPStatus.OK)
    except ResourceNotFoundError as err:
        return func.HttpResponse(str(err.message), status_code=HTTPStatus.NOT_FOUND)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
