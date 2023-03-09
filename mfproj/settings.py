"""
Django settings for mfproj project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_check_seo',
    'cms',
    'menus',
    'treebeard',
    'captcha',
    'storages',
    'robots',
    'webmaster_verification',
    #created apps
    'home.apps.HomeConfig',
    'music.apps.MusicConfig',
    'galleries.apps.GalleriesConfig',
    'mfevents.apps.MfeventsConfig',
]

SITE_ID = 1
ROBOTS_USE_SCHEME_IN_HOST = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'mfproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mfproj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASE_URL = config('DATABASE_URL')

DATABASES = {
    #'default': {
     #   'ENGINE': 'django.db.backends.sqlite3',
      #  'NAME': BASE_DIR / 'db.sqlite3',
    #}
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('PORT', cast=int),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# FORM SUBMISSION
# Comment out the following line and place your railway URL, and your production URL in the array.
#

CSRF_TRUSTED_ORIGINS = [#'https://web-production-22f3.up.railway.app',
                        #'https://web-production-22f3.up.railway.app/admin',
                        'https://*web-production-22f3.up.railway.app',
                        'https://*morefireouternational.com',
                        ]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGES = [
    ('en', 'English'),
]
LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

S3_ENABLED = config('S3_ENABLED', cast=bool, default=False)
LOCAL_SERVE_MEDIA_FILES = config('LOCAL_SERVE_MEDIA_FILES', cast=bool, default=not S3_ENABLED)
LOCAL_SERVE_STATIC_FILES = config('LOCAL_SERVE_STATIC_FILES', cast=bool, default=not S3_ENABLED)

if (not LOCAL_SERVE_MEDIA_FILES or not LOCAL_SERVE_STATIC_FILES) and not S3_ENABLED:
    raise ValueError('S3_ENABLED must be true if either media or static files are not served locally')

if S3_ENABLED:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_REGION')
    AWS_DEFAULT_ACL =  'public-read'
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ENDPOINT_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_LOACATION = 'static'
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        'Access-Control-Allow-Origin': '*',
    }

if not LOCAL_SERVE_STATIC_FILES:
    STATIC_DEFAULT_ACL = 'public-read'
    STATIC_LOCATION = 'static/'
    STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'utils.storage_backends.StaticStorage'

if not LOCAL_SERVE_MEDIA_FILES:
    PUBLIC_MEDIA_DEFAULT_ACL = 'public-read'
    PUBLIC_MEDIA_LOCATION = 'media/public/'

    MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'utils.storage_backends.PublicMediaStorage'

    PRIVATE_MEDIA_DEFAULT_ACL = 'private'
    PRIVATE_MEDIA_LOCATION = 'media/private/'
    PRIVATE_FILE_STORAGE = 'utils.storage_backends.PrivateMediaStorage'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

#Email Settings
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
#EMAIL_USE_SSL = config('EMAIL_HOST_SSL')

WEBMASTER_VERIFICATION = {
    #'bing': '<bing verification code>',
    'google': config('GOOGLE_VERIFY'),
    #'majestic': '<majestic verification code>',
    #'yandex': '<yandex verification code>',
    #'alexa': '<alexa verification code>',
}

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',

        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
"""
