"""
Django settings for crm project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j#*f!&5bggc!r9gmnozitz0^%vj_(k71t2+=o-f=fgfs39%k3*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['vcm-crm.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contact_management',
    'anymail',
    'django_tables2',
    'django_filters',
    'bootstrap4',
    'bootstrapform',
    'bootstrap_modal_forms',
    'chartjs',
    'webhooks',
    'formtools',
    "sorl.thumbnail",
    'django.contrib.humanize',

]

MIDDLEWARE = [

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crm.urls'

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

WSGI_APPLICATION = 'crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR,'mediafiles')
MEDIA_URL = '/mediafiles/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
    
if DEBUG: 
   STATIC_ROOT = os.path.join(BASE_DIR, '/staticfiles')
else:
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"  # or sendgrid.EmailBackend, or...
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD',None)
EMAIL_HOST_USER= os.environ.get('EMAIL_HOST_USER',None)
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY',None)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL',None) # if you don't already have this in settings
SERVER_EMAIL = os.environ.get('SERVER_EMAIL',None)
ANYMAIL_WEBHOOK_SECRET = os.environ.get('ANYMAIL_WEBHOOK_SECRET',None)
GITHUB_WEBHOOK_KEY = os.environ.get('GITHUB_WEBHOOK_KEY',None)
EMAIL_PORT = 587

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['email'] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("EMAIL_DB_NAME",None),
        "USER": os.environ.get("EMAIL_DB_USER",None),
        "PASSWORD": os.environ.get("EMAIL_DB_PASSWORD",None),
        "HOST": os.environ.get("EMAIL_DB_HOST",)
        "PORT": 5432,
    }
try:
    from .local_settings import *
    print('local_settings__in the mf')

except ImportError:
    pass