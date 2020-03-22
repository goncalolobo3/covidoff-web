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

COVIDOFF_MAXIMUM_BROADCAST_MESSAGE_SIZE = 32768

COVIDOFF_HEALTHCARE_DEPLOY = False
COVIDOFF_GOVERNMENT_DEPLOY = not COVIDOFF_HEALTHCARE_DEPLOY

if COVIDOFF_GOVERNMENT_DEPLOY == COVIDOFF_HEALTHCARE_DEPLOY:
    raise ImproperlyConfigured("Choose either COVIDOFF_HEALTHCARE_DEPLOY or COVIDOFF_GOVERNMENT_DEPLOY in the settings file, both cannot be set")

COVIDOFF_MESSAGES_PER_PAGE = 3 # 25
COVIDOFF_USERS_PER_PAGE = 3 # 25

if COVIDOFF_HEALTHCARE_DEPLOY:
    LOGIN_REDIRECT_URL = '/tracker/'

elif COVIDOFF_GOVERNMENT_DEPLOY:
    LOGIN_REDIRECT_URL = '/broadcast/'

COVIDOFF_SIGNING_KEY = b'6dc86c1c43c8fdadca648183af6c6ab872cff7a7fd61e4967f7d177253645768'
COVIDOFF_VERIFY_KEY = b'a0d096e50dd19dcd98611132b2ab8dce16ab90a8e88804164b657eb02c6b97aa'

LOGIN_URL = '/account/login/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v9b2hl1&yn7n(e#5*mrqf#(n6=bly3q&ee3mnr8-m^3s46ye12'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
    'tracker',
]

if COVIDOFF_HEALTHCARE_DEPLOY:
    INSTALLED_APPS += ['qr_code']

if COVIDOFF_GOVERNMENT_DEPLOY:
    INSTALLED_APPS += ['broadcast']

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
]
