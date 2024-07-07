from dotenv import load_dotenv
import os


load_dotenv()

connection_string = os.getenv("CONNECTION_STRING")
excel_connection_string = os.getenv("EXCEL_CONNECTION_STRING")
http_trigger_url = os.getenv("HTTP_TRIGGER_URL")
deleted_accounts_table = os.getenv("DELETED_ACCOUNTS_TABLE")
documentation_table = os.getenv("DOCUMENTATION_TABLE")
main_manager = os.getenv("MAIN_MANAGER")
