import config.config_variables
import string
import secrets
import re

from .azure_client import AzureClient


class NewUser:
    def __init__(self, user_details):
        self.email_suffix = config.config_variables.email_suffix
        self.department = config.config_variables.department
        self.mail_nick_name = self.get_mail_nick_name(user_details)
        self.details = self.get_request_details(
            self.mail_nick_name, user_details["expiration_date"]
        )
        self.azure_client = AzureClient()

    def add_user(self):
        access_token = self.azure_client.create_access_token()
        response = self.azure_client.add_user(self.details, access_token)
        return response

    def get_request_details(self, mail_nick_name, expiration_date):
        return {
            "accountEnabled": True,
            "displayName": mail_nick_name,
            "mailNickname": mail_nick_name,
            "userPrincipalName": mail_nick_name + self.email_suffix,
            "passwordProfile": {
                "forceChangePasswordNextSignIn": True,
                "password": self.generate_strong_password(),
            },
            "department": self.department,
            "employeeType": expiration_date,
        }

    def get_mail_nick_name(self, details):
        return (
            details["first_name"][0]
            + details["last_name"][0]
            + details["identity"][-6:]
        ).upper()

    def generate_strong_password(self, length=12):
        alphabet = string.ascii_letters + string.digits
        while True:
            password = "".join(secrets.choice(alphabet) for _ in range(length))
            if self.is_strong_password(password):
                return password

    def is_strong_password(self, password):
        return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", password) is not None
