import os
from dotenv import load_dotenv

load_dotenv()

# host
HOST = os.environ.get("HOST")

# database
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

# google auth
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_REDIRECT_URL = f"{HOST}/{os.environ.get('CLIENT_REDIRECT_PATH')}"
