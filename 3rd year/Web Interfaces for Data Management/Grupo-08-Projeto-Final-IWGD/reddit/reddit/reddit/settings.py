"""
Django settings for reddit project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-26*qn$1_h)v385c#x*9^+w^gwc+%j7e81l@#tmim1t7b(0xvj#'

# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = True # para produção

DEBUG = True
ALLOWED_HOSTS=['*']


try:
    import six

except ImportError:

    if not os.getenv("SIX_INSTALL_ATTEMPTED") == "1":

        print("Trying to install required module: six\n")
        os.environ['SIX_INSTALL_ATTEMPTED'] = "1"
        os.system('pip install six')
    else:
        print("Failed to install six. Please install it manually")

try:
    import openai

except ImportError:

    if not os.getenv("OPENAI_INSTALL_ATTEMPTED") == "1":

        print("Trying to install required module: openai\n")
        os.environ['OPENAI_INSTALL_ATTEMPTED'] = "1"
        os.system('pip install openai==0.28.1')
    else:
        print("Failed to install openai. Please install it manually")


try:
    import whitenoise

except ImportError:

    if not os.getenv("WHITENOISE_INSTALL_ATTEMPTED") == "1":

        print("Trying to install required module: whitenoise\n")
        os.environ['WHITENOISE_INSTALL_ATTEMPTED'] = "1"
        os.system('pip install whitenoise')
    else:
        print("Failed to install whitenoise. Please install it manually")


try:
    import captcha

except ImportError:

    if not os.getenv("DJANGO__RECAPTCHA_INSTALL_ATTEMPTED") == "1":

        print("Trying to install required module: django-simple-captcha\n")
        os.environ['DJANGO__RECAPTCHA_INSTALL_ATTEMPTED'] = "1"
        os.system('pip install django-simple-captcha')
        os.system('pip install django-recaptcha')

    else:
        print("Failed to install captcha dependencies: django-simple-captcha and django-recaptcha. Please install it "
              "manually")

    try:
        import requests

    except ImportError:

        if not os.getenv("REQUESTS_INSTALL_ATTEMPTED") == "1":

            print("Trying to install required module: requests\n")
            os.environ['REQUESTS_INSTALL_ATTEMPTED'] = "1"
            os.system('pip install requests')
        else:
            print("Failed to install requests. Please install it manually")







STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'subreddit/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'subreddit/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'subreddit/static/media')

SERVE_MEDIA_FILES = True

# Application definition

RECAPTCHA_PUBLIC_KEY = '6Lf5eYooAAAAAMFeToVnju1T74nrOyq256ejv1m3'
RECAPTCHA_PRIVATE_KEY = '6Lf5eYooAAAAALU7LfNVg7Hhm3Jr2lQ_W9Tk3c-F'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

SITE_ID = 2

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'subreddit.apps.SubredditConfig',
    'captcha',
    'django.contrib.sites',
    "allauth",
    'allauth.account',
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]



SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],
        "AUTH_PARAMS": {"access_type": "online"}

    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reddit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'reddit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'