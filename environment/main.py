from environment.variables import EnvironmentVariable
from environment.base import *
from datetime import timedelta

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': EnvironmentVariable.DATABASE_NAME,
        'HOST': EnvironmentVariable.DATABASE_HOST,
        'PORT': EnvironmentVariable.DATABASE_PORT,
        'USER': EnvironmentVariable.DATABASE_USERNAME,
        'PASSWORD': EnvironmentVariable.DATABASE_PASSWORD,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


AUTH_USER_MODEL = "user.User"


ALLOWED_HOSTS = ["*"]

if EnvironmentVariable.DEBUG == "True":
    ALLOWED_HOSTS.append("127.0.0.1")


# JWT Configuration
JWT_SECRET_KEY = EnvironmentVariable.JWT_SECRET_KEY
JWT_ALGORITHM = "HS256"


# Cipher Configurations
CIPHER_SECRET_KEY = EnvironmentVariable.AES_SECRET_KEY
CIPHER_BLOCK_SIZE = 16

# Simple JWT Configurations
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2)
}
