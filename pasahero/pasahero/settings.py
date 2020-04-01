"""
Django settings for pasahero project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    SECRET_KEY = 'p1w4t09utvu2wiggduadxe02y6ht88g9!2i=295p#xyf0f%@e('
else:
    SECRET_KEY = os.environ.get('PASAHERO_SECRET_KEY')

ALLOWED_HOSTS = ["127.0.0.1",
"18.139.209.193",
"ec2-18-139-209-193.ap-southeast-1.compute.amazonaws.com",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cities',
    'transportations',
    'commuters',
    'documents',
    'employees',
    'preferred_times',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pasahero.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'pasahero.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            # in testing
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
        'default': {
            # remote ElephantSQL db. only use in deployment
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('PASAHERO_DATABASE_NAME'),
            'USER': os.environ.get('PASAHERO_DATABASE_USER'),
            'PASSWORD':os.environ.get('PASAHERO_DATABASE_PASSWORD'),
            'HOST':os.environ.get('PASAHERO_DATABASE_HOST'),
            'PORT':'5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL = '/login'


if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = STATIC_DIR
    MEDIA_URL = '/media/'
    MEDIA_ROOT = MEDIA_DIR
else:
    AWS_ACCESS_KEY_ID = os.environ.get('PASAHERO_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('PASAHERO_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('PASAHERO_AWS_STORAGE_BUCKET_NAME')

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'