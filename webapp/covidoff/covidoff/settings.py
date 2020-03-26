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

COVIDOFF_MAXIMUM_BROADCAST_MESSAGE_SIZE = os.environ.get('COVIDOFF_MAXIMUM_BROADCAST_MESSAGE_SIZE', 32768)

COVIDOFF_DEPLOYMENT_TYPE = os.environ.get('COVIDOFF_DEPLOYMENT_TYPE', 'gov')

if COVIDOFF_DEPLOYMENT_TYPE == 'htc':
    COVIDOFF_HEALTHCARE_DEPLOY = True
    COVIDOFF_GOVERNMENT_DEPLOY = False
    COVIDOFF_AUTHENTICATION_DEPLOY = False

elif COVIDOFF_DEPLOYMENT_TYPE == 'gov':
    COVIDOFF_HEALTHCARE_DEPLOY = False
    COVIDOFF_GOVERNMENT_DEPLOY = True
    COVIDOFF_AUTHENTICATION_DEPLOY = False

elif COVIDOFF_DEPLOYMENT_TYPE == 'auth':
    COVIDOFF_HEALTHCARE_DEPLOY = False
    COVIDOFF_GOVERNMENT_DEPLOY = False
    COVIDOFF_AUTHENTICATION_DEPLOY = True

else:
    raise ImproperlyConfigured("Deployment type environment variable not found or invalid. Set COVIDOFF_DEPLOYMENT_TYPE to either healthcare deployment (htc) or government deployment (gov) in your environment.")

COVIDOFF_MESSAGES_PER_PAGE = os.environ.get('COVIDOFF_MESSAGES_PER_PAGE', 25)
COVIDOFF_USERS_PER_PAGE = os.environ.get('COVIDOFF_USERS_PER_PAGE', 25)

COVIDOFF_TOPIC_NAME = os.environ.get('COVIDOFF_TOPIC_NAME', 'covidoff')

if COVIDOFF_HEALTHCARE_DEPLOY:
    LOGIN_REDIRECT_URL = '/tracker/'

elif COVIDOFF_GOVERNMENT_DEPLOY:
    LOGIN_REDIRECT_URL = '/broadcast/'

COVIDOFF_SIGNING_KEY = os.environ.get('COVIDOFF_SIGNING_KEY', b'be5e8d34555c7d686c0c7bfe393becc83bbec8df2ab4aeae89d7af4046b1335d')
COVIDOFF_VERIFY_KEY = os.environ.get('COVIDOFF_VERIFY_KEY', b'514e9c0b9beb7cf38f3c26f9d533f35e7ac80de8b757c84285933c8b1260e4b3')

LOGIN_URL = '/account/login/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
]

if COVIDOFF_AUTHENTICATION_DEPLOY:
    INSTALLED_APPS += ['authnoop']

else:

    AUTH_USER_MODEL = 'access.User'

    INSTALLED_APPS += [
        'access',
        'tracker'
    ]

    if COVIDOFF_HEALTHCARE_DEPLOY:
        INSTALLED_APPS += ['qr_code']

    if COVIDOFF_GOVERNMENT_DEPLOY:
        INSTALLED_APPS += [
            'broadcast'
        ]

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

        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'postgres',
        # 'USER': 'postgres',
        # 'PASSWORD': 'mysecretpassword',
        # 'HOST': 'db',
        # 'PORT': '5432',
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
