from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('TEST_DB_NAME'),
        'USER': config('TEST_DB_USER'),
        'PASSWORD': config('TEST_DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432'
    }
}
