from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME_TEST'),
        'USER': config('DB_USER_TEST'),
        'PASSWORD': config('DB_PASSWORD_TEST'),
        'HOST': 'db',
        'PORT': '5432'
    }
}
