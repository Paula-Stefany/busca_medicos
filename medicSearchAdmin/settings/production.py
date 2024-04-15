from .settings import *
import os 
from dotenv import load_dotenv

load_dotenv()
DEBUG = False
PRODUCTION_KEY = os.getenv('PRODUCTION_KEY')

# crie a secret key para seu ambiente de produção
SECRET_KEY = PRODUCTION_KEY

# alterar para o IP do ambiente de produção quando houver
ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
