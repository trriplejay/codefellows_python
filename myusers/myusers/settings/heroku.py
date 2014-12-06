from base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

# Honor the 'X=Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

STATIC_ROOT = 'staticfiles'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# settings for heroku
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'dj_database_url.config()',
    }
}
DATABASES['default'] = dj_database_url.config()