import requests
import json
import config.config_variables
import msal


class AzureClient:
    def __init__(self):
        self.client_id = config.config_variables.azure_client_id
        self.client_secret = config.config_variables.azure_client_secret
        self.tenant_id = config.config_variables.azure_tenant_id
        self.graph_url = config.config_variables.graph_url

    def create_access_token(self):
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        scope = ["https://graph.microsoft.com/.default"]
        app = msal.ConfidentialClientApplication(
            self.client_id, authority=authority, client_credential=self.client_secret
        )
        result = app.acquire_token_for_client(scopes=scope)
        if "access_token" in result:
            return result["access_token"]
        else:
            return "error creating access token"

    def add_user(self, user, token):
        try:
            response = requests.post(
                f"{self.graph_url}/users",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(user),
            )
            response.raise_for_status()
            return {
                "username": response.json().get("userPrincipalName"),
                "password": user["passwordProfile"]["password"],
                "code": "200",
            }
        except requests.HTTPError as e:
            if (
                response.status_code == 400
                and "userPrincipalName already exists"
                in response.json().get("error", {}).get("message", "")
            ):
                return {"username": user["userPrincipalName"], "code": "400"}
            return {
                "username": user["userPrincipalName"],
                "code": e.response.status_code,
            }
