"""
Django settings for timesheet project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DJANGO ADMIN
ADMINS = (
    # ('Administrator', 'suporte@lernasnuvens.pt'),
)

MANAGERS = ADMINS

SITE_NAME = 'Timesheet'

# This is how you can define name of your site
SITE_DIR = 'main_site'

# The hostname of the Booktype server (e.g. www.myserver.org, 192.168.1.10, booktype.myserver.org)
SERVER = 'timesheet.dikegroup.com'

ROOT = Path(os.path.abspath(__file__)).ancestor(2)

URL = 'https://{}'.format(SERVER)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')u9$$9*#_w-6cj*2nub5gbw*g&-yb04u%*6h46k!-s=-(s8lwk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# E-MAIL OPTIONS
DEFAULT_FROM_EMAIL = 'suporte@lernasnuvens.pt'
REPORT_EMAIL_USER = 'suporte@lernasnuvens.pt'

# E-MAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '192.168.1.4'
EMAIL_PORT = 25
# EMAIL_HOST_USER = 'booktype@' + THIS_BOOKTYPE_SERVER
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False

# DJANGO STUFF
# AUTH_PROFILE_MODULE = 'account.UserProfile'

TIME_ZONE = 'Europe/Lisbon'

LANGUAGE_CODE = 'pt'

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('American English')),
    ('en-gb', gettext('British English')),
    ('ca', gettext('Català')),
    ('cs', gettext('Česky')),
    ('de', gettext('Deutsch')),
    ('de-at', gettext('Österreichisches Deutsch')),
    ('el', gettext('Ελληνικά')),
    ('es', gettext('Español')),
    ('fr', gettext('Français')),
    ('it', gettext('Italiano')),
    ('ja', gettext('日本語')),
    ('ko-kr', gettext('한국어')),
    ('hu', gettext('Magyar')),
    ('nl', gettext('Nederlands')),
    ('nb', gettext('Norsk (Bokmål)')),
    ('pl', gettext('Polski')),
    ('pt', gettext('Português')),
    ('pt-br', gettext('Português do Brasil')),
    ('ru', gettext('Русский')),
    ('sq', gettext('Shqipe')),
    ('fi', gettext('Suomi')),
    ('tr', gettext('Türkçe')),
    ('uk-ua', gettext('українська мова')),
)

STATIC_ROOT = ROOT.child('static')

STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# data
DATA_ROOT = ROOT.child('data')
DATA_URL = '{}/data/'.format(URL)

# Application definition

INSTALLED_APPS = [

    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Compressor
    "compressor",

    # Chronos Apps
    'apps.core',
    'apps.account',
    'apps.client',
    'apps.project',
    'apps.task',
    'apps.entry',
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

ROOT_URLCONF = '{}.urls'.format('main_site')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True
        },
    },
]

WSGI_APPLICATION = '{}.wsgi.application'.format('main_site')


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

LOCALE_PATHS = (
    ROOT.child('locale'),
)