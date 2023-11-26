from .base import *

config = useConfig('local')

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
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('AWS_ACCESS_KEY')

EMAIL_HOST_PASSWORD = config('AWS_SECRET')
