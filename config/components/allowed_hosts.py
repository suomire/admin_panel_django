import os
from dotenv import load_dotenv

load_dotenv("config/.env")


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(" ")
