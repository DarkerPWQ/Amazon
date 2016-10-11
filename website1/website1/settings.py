# -*- coding: utf-8 -*-
"""
Django settings for website1 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#这个BASE_DIR 是变量值项目的根目录，也就是settings.py的存放位置。


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%b=l*#ye-y$2#zx^2vnvr-7v#107e_l_8mlxvun99yc@^$+*2$'
import djcelery
djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_TIMEZONE="Asia/Shanghai"
from datetime import timedelta

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# CELERYBEAT_SCHEDULE = {
#     # Executes every Monday morning at 7:30 A.M
#     'add-every-10-seconds': {
#         'task': 'blog.tasks.Timing_task',
#         #'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         #'schedule': crontab(minute='*/1'),
#         'schedule': timedelta(seconds=6),
#         'args': (),
#     },
# }

#调度器
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'djcelery',
    'kombu.transport.django',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'

)

ROOT_URLCONF = 'website1.urls'

WSGI_APPLICATION = 'website1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',#数据库
         # 'NAME':'pwq'
        
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3')

        #'NAME':'myhyy',
        #'USER':'pwq',
        #'PASSWORD':'pwqagwt1314ysys',
        #'HOST':'myhyy.crspo0qkrwct.eu-west-1.rds.amazonaws.com',
        'NAME':'maizi2',
        'USER':'root',
        'PASSWORD':'1234',
        'HOST':'127.0.0.1',
        'PORT':'3306'
    }
}
# Internationalization
AUTH_USER_MODEL = 'blog.User'
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
CELERY_TIMEZONE = TIME_ZONE
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# #然后给静态文件变量赋值，告诉Django，静态文件在哪里，是静态文件的路劲
STATICFILES_DIRS = (
('css',os.path.join(STATIC_ROOT,'css').replace('\\','/') ),
    ('js',os.path.join(STATIC_ROOT,'js').replace('\\','/') ),
    ('images',os.path.join(STATIC_ROOT,'images').replace('\\','/') ),
    ('video',os.path.join(STATIC_ROOT,'video').replace('\\','/') ),
    ('src',os.path.join(STATIC_ROOT,'src').replace('\\','/') ),
('Js',os.path.join(STATIC_ROOT,'Js').replace('\\','/') ),
('Image',os.path.join(STATIC_ROOT,'Image').replace('\\','/') ),

)
# # STATICFILES_DIRS = (
# #     os.path.join(BASE_DIR, "static"),
# #     '/path/to/others/static/',
# # )
STATICFILES_FINDERS = (
   "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)
