# Application definition
import os
from dotenv import load_dotenv

load_dotenv("config/.env")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies.apps.MoviesConfig',

]

if os.environ.get('DEBUG', False):
    INSTALLED_APPS += ['debug_toolbar']
