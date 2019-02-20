"""
Django settings for main_website project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',
        '-&%4hhs)233(_fdbba23+sda23@16!~nadsasd^fab98x9c_cl#009ad3-91')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DJANGO_DEBUG', True))

ALLOWED_HOSTS = [
    '*',
    '.***.com',
    '127.0.0.1',
    '.herokuapp.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # added for allauth
    'django.contrib.sites', 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'stripe',

    # added Crossway demo apps
    'accounts',
    'products',
    'shopping_cart',
    'esv_search.apps.esv_searchConfig'
    
]

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

ROOT_URLCONF = 'main_website.urls'

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

WSGI_APPLICATION = 'main_website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'


# Add to test email:
SEND_GRID_API_KEY = ''
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

VENV_PATH = os.path.dirname(BASE_DIR)

# URL to use when referring to where static files are served from
STATIC_URL = '/static/'

# Absolute path to directory where collectstatic will collect static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(VENV_PATH, 'media_root')

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Heroku Settings for Django
"""
# Update database configuration from $DATABASE_URL.

DATABASES['default'].update(dj_database_url.config(
        conn_max_age=600, ssl_require=True))
"""

django_heroku.settings(locals())

# ESV API settings

API_KEY = 'c301f49b5000085fafc0dfb1d696d8855e78a46a'
API_SEARCH_URL = 'https://api.esv.org/v3/passage/search/'
API_TEXT_URL = 'https://api.esv.org/v3/passage/text/'

API_HEADERS = {
    'Accept': 'application/json',
    'Authorization': 'Token %s' % API_KEY
}

API_OPTIONS = {
    'include-passage-references': 'false',
    'include-first-verse-numbers': 'false',
    'include-verse-numbers': 'false',
    'include-footnotes': 'false',
    'include-footnote-body': 'false',
    'include-short-copyright': 'false',
    'include-passage-horizontal-lines': 'false',
    'include-heading-horizontal-lines': 'false',
    'include-headings': 'false',
    'include-selahs': 'false',
    'indent-paragraphs': '0',
    'indent-poetry': 'false',
    'indent-poetry-lines': '0',
    'indent-declares': '0',
    'indent-using': 'tab',
    'indent-psalm-doxology': '0',
    'line-length': '0'
}

# Stripe and Braintree Settings

if DEBUG:
    # test keys
    STRIPE_PUBLISHABLE_KEY = 'pk_test_KA6Cf0oC5c235Qa63SAZrrAF'
    STRIPE_SECRET_KEY = 'sk_test_MANe2GKDofSF7dTiS7rsvHvg'
    BT_ENVIRONMENT='sandbox'
    BT_MERCHANT_ID='h7bvbc2hfv38qzcv'
    BT_PUBLIC_KEY='z6m9n9x4429njpq7'
    BT_PRIVATE_KEY='def748a813a207e7db6b0f8d2d6ffcd5'
else:
    # live keys
    STRIPE_PUBLISHABLE_KEY = 'pk_test_KA6Cf0oC5c235Qa63SAZrrAF'
    STRIPE_SECRET_KEY = 'sk_test_MANe2GKDofSF7dTiS7rsvHvg'

# Django AllAuth Settings

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/products'