#coding=utf-8
"""
Django settings for hwtb project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gyfm@@ap+#eo859jg67e^ny$+rd&83s+91b8u5v*^y4vsi0r29'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'www.apps.WwwConfig',
	'ckeditor',
    'ckeditor_uploader',
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hwtb.urls'

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

WSGI_APPLICATION = 'hwtb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hwtb',
	'USER': 'hwtb',
	'PASSWORD': 'biscuits@1',
	'HOST': '127.0.0.1',
	'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#APPEND_SLASH=False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'

LOCALE_PATHS = (os.path.join(BASE_DIR, "www/locale"),
                os.path.join(BASE_DIR, "hwtb/locale"))

# ckeditor
CKEDITOR_UPLOAD_PATH = "ckeditor_upload"
CKEDITOR_BROWSER_PATH = "ckeditor_browse"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS={
    'default':{
        'skin': 'moono',
        'toolbar_Basic': [
                          ['Source', '-', 'Bold', 'Italic']
                          ],
        'toolbar_Full': [
                        ['div','Source','-','Save','NewPage','Preview','-','Templates'], 
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'], 
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'], 
            ['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'], 
            ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'], 
            ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'], 
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'], 
            ['Link','Unlink','Anchor'], 
            ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'], 
            ['Styles','Format','Font','FontSize'], 
            ['TextColor','BGColor'], 
            ['Maximize','ShowBlocks','-','About', 'pbckcode'],
        ],
        'toolbar': 'Full',
        'height': 291,
        'width': 835,
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
        'filebrowserUploadUrl':'/www/upload/',
        'filebrowserBrowseUrl':'/www/browser/'
    },
}
CKEDITOR_EXTRAPLUGS_CONFIG = ['uploadimage']
CKEDITOR_EXTRAPLUGS_RESOURCES_CONFIG =[['uploadimage','img_uploads/%Y%m%d','']]
#log
'''
LOGGING ={
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
                'format': '%(levelname)s %(asctime)s %(message)s'
                },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'admin_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'/var/log/web.admin',
            'formatter':'standard',
        },
        'www_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'/var/log/web.www',
            'formatter':'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'admin':{
            'handlers': ['admin_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'www':{
            'handlers': ['www_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
'''
