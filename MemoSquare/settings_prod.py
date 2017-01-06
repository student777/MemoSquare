from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'memosquare',
        'USER': 'memosquare',
        'PASSWORD': 'cleancode',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# deploy settings
ALLOWED_HOSTS = [
    'memo-square.com',
]

DEBUG = False

# Cross-Origin Resource Sharing settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'GET',
    'OPTIONS',
    'POST',
)
CORS_ORIGIN_WHITELIST = (
    'chrome-extension://njlkefpcpojddmjihelliajgkhdgcoea/res/popup.html',
)
