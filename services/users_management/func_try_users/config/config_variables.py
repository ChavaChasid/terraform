import os
from dotenv import load_dotenv

load_dotenv()

email_suffix = os.getenv("EMAIL_SUFFIX")
department = os.getenv("DEPARTMENT")
azure_tenant_id = os.getenv("AZURE_TENANT_ID")
azure_client_id = os.getenv("AZURE_CLIENT_ID")
azure_client_secret = os.getenv("AZURE_CLIENT_SECRET")
graph_url = os.getenv("GRAPH_URL")
