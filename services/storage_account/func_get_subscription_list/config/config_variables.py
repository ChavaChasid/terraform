from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv("CONNECTION_STRING")
documentation_table = os.getenv("DOCUMENTATION_TABLE")
