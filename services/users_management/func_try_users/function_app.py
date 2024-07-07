import azure.functions as func
import logging
import json
from project.new_user import NewUser

app = func.FunctionApp()

@app.function_name(name="HttpTrigger1")
@app.route(route = "")
def add_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        new_user = NewUser(req_body)
        res = new_user.add_user()
    except ValueError:
        res = "Internal Server Error"

    return func.HttpResponse(json.dumps(res))
