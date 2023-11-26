from .base import *

config = useConfig('test')

# CORS

CORS_ORIGIN_WHITELIST = [
    config('CLIENT_URL')
]

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432'
    }
}
