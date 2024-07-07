from dotenv import load_dotenv
import os

load_dotenv()

workspace_id = os.getenv("WORKSPACE_ID")
tenant_id = os.getenv("TENANT_ID_LA")
client_id = os.getenv("CLIENT_ID_LA")
client_secret = os.getenv("CLIENT_SECRET_LA")
