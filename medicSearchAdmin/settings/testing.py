from .settings import *
from dotenv import load_dotenv


load_dotenv()
DEBUG = True
TESTING_KEY= os.getenv('TESTING_KEY')

# crie a secret key para ambiente de teste
SECRET_KEY = 'uihYHY*&¨Gyuvyuyt¨%$%ÖIj)()-i_jIUG#$sexDcFtdrtfvGBHJBuyg677BYTR$¨huyg&¨gyH7656T&ÿ7gUuuyg'

# alterar para o IP do ambiente de teste quando houver
ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite'),
    }
}
