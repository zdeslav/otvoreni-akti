"""
Django settings for otvoreni_akti project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env(  # set default values and casting
    DEBUG=(bool, False),
    DEPLOYMENT=(str, 'prod'),
    SECRET_KEY=(str, '9c-cjj9*1idd#prb#+1%=a1&&avhk2po#*5u$(=4-cj28!3+6*'),
)

# Build paths inside the project like this: base('desired/local/path')
# - the path containing manage.py
#   (e.g. ~/code/posterbat)
base = environ.Path(__file__) - 2  # two folders back (/a/b/ - 2 = /)
BASE_DIR = base()
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# - the Django project root containing settings.py
# (e.g. ~/code/posterbat/posterbat)
root = environ.Path(__file__) - 1
PROJECT_ROOT = root()
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(env_file=base('.env'))  # reading .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')  # default used if not in os.environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')  # False if not in os.environ

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'akti.za-grad.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_elasticsearch_dsl',
    'svg',
    'otvoreni_akti.apps.search',
    'otvoreni_akti.apps.scraper',
]

# Default host for Elasticsearch
# we need either ELASTICSEARCH_URL (Dokku) or BONSAI_URL (Heroku)
try:
    ES_URL = env.str('ELASTICSEARCH_URL')
except ImproperlyConfigured:
    ES_URL = env('BONSAI_URL')

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': ES_URL
    },
}

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

ROOT_URLCONF = 'otvoreni_akti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'otvoreni_akti.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db(),
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
# set your local time zone to more easily analyse data on the backend
TIME_ZONE = 'CET'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = root('staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (base('otvoreni_akti/static'),)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Celery settings
from celery.schedules import crontab

CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'scrape-everything-per-schedule': {
        'task': 'otvoreni_akti.apps.scraper.tasks.celery_scrape_everything',
        'schedule': crontab(minute=0, hour=4),
    },
    'rescrape-last-n-periods-per-schedule': {
        'task': 'otvoreni_akti.apps.scraper.tasks.celery_rescrape_last_n',
        'schedule': crontab(minute=0, hour=0),
    },
}

# Sentry settings
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://ecf4aa705eee46a7abbbbf80a0d43018@o397377.ingest.sentry.io/5251765",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Custom variables
ACTS_ROOT_URL = 'http://web.zagreb.hr'
SITE_ID = 1
RESCRAPE_LAST_N_PERIODS = 5
MAX_SEARCH_RESULTS = 1000
SEARCH_REQUEST_TIMEOUT = 30     # In seconds
