"""
Django settings for covidoff project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from django.core.exceptions import ImproperlyConfigured
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _raise(ex):
    raise ex

#
# ARN for an SNS Topic.
#
# See https://sa-east-1.console.aws.amazon.com/sns/v3/home
#
COVIDOFF_SNS_TOPIC_ARN = os.environ.get('COVIDOFF_SNS_TOPIC_ARN', 'arn:aws:sns:sa-east-1:494854379016:covidoff-colombia') or _raise(ImproperlyConfigured('COVIDOFF_SNS_TOPIC_ARN is not set'))

#
# AWS Region name, where the SNS service is deployed.
#
COVIDOFF_AWS_REGION_NAME = os.environ.get('COVIDOFF_AWS_REGION_NAME', 'sa-east-1') or _raise(ImproperlyConfigured('COVIDOFF_SNS_TOPIC_ARN is not set'))

#
# Number of messages per page
#
COVIDOFF_MESSAGES_PER_PAGE = os.environ.get('COVIDOFF_MESSAGES_PER_PAGE', 25)

#
# Number of users per page
#
COVIDOFF_USERS_PER_PAGE = os.environ.get('COVIDOFF_USERS_PER_PAGE', 25)

#
# Signing and verification keys
#
# TODO document how to generate keys
# 
#
COVIDOFF_SIGNING_KEY = os.environ.get('COVIDOFF_SIGNING_KEY', 'be5e8d34555c7d686c0c7bfe393becc83bbec8df2ab4aeae89d7af4046b1335d') or _raise(ImproperlyConfigured('COVIDOFF_SIGNING_KEY is not set'))
COVIDOFF_VERIFY_KEY = os.environ.get('COVIDOFF_VERIFY_KEY', '514e9c0b9beb7cf38f3c26f9d533f35e7ac80de8b757c84285933c8b1260e4b3') or _raise(ImproperlyConfigured('COVIDOFF_VERIFY_KEY is not set'))

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/broadcast/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '1+*q1@5$+r)rffyvefj=wgv@c%1*-!hfb0xz%6&e4v#)_ek@kt')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'access.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'access',
    'broadcast',
    'authnoop'
]

AUTH_USER_MODEL = 'access.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'covidoff.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'covidoff.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'mysecretpassword',
            'HOST': 'db',
            'PORT': '5432',
        }
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

LANGUAGES = (
    ('en', 'English'),
    ('pt', 'Portugês'),
    ('es', 'Español')
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Add these new lines
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

from django.core.serializers import BUILTIN_SERIALIZERS

BUILTIN_SERIALIZERS['json'] = 'covidoff.serializers'
