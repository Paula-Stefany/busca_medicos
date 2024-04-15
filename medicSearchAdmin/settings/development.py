from .settings import *
import os 
from dotenv import load_dotenv


load_dotenv()
DEBUG = True
DEVELOPMENT_KEY = os.getenv('DEVELOPMENT_KEY')

# crie a secret key para seu ambiente de desenvolvimento
SECRET_KEY = DEVELOPMENT_KEY

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
