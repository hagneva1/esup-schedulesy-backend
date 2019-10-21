# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

# In your virtualenv, edit the file $VIRTUAL_ENV/bin/postactivate and set
# properly the environnement variable defined in this file (ie: os.environ[KEY])
# ex: export DEFAULT_DB_NAME='project_name'

# Default values for default database are :
# engine : sqlite3
# name : PROJECT_ROOT_DIR/default.db


DATABASES['default']['HOST'] = environ.get('DB_HOST')
DATABASES['default']['USER'] = environ.get('DB_USER')
DATABASES['default']['PASSWORD'] = environ.get('DB_PWD')
DATABASES['default']['NAME'] = environ.get('DB_NAME')

DATABASES['ade']['HOST'] = environ.get('ADE_DB_HOST')
DATABASES['ade']['USER'] = environ.get('ADE_DB_USER')
DATABASES['ade']['PASSWORD'] = environ.get('ADE_DB_PWD')
DATABASES['ade']['NAME'] = environ.get('ADE_DB_NAME')


############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '*'
]

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', '%s.log' % SITE_NAME)))
LOGGING['handlers']['infocentre_file']['filename'] = environ.get('LOG_DIR',
        normpath(join('/tmp', 'infocentre_%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'
LOGGING['handlers']['infocentre_file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


###########################
# Unit test configuration #
###########################

INSTALLED_APPS += [
    'coverage',
    'debug_toolbar',
]

#################
# Debug toolbar #
#################

DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']


################
# ADE settings #
################

ADE_WEB_API['USER'] = environ.get('ADE_WS_USER')
ADE_WEB_API['PASSWORD'] = environ.get('ADE_WS_PASSWORD')
ADE_WEB_API['HOST'] = environ.get('ADE_WS_HOST')
ADE_WEB_API['PROJECT_ID'] = environ.get('ADE_PROJECT_ID')

#########
# STAGE #
#########

STAGE = 'dev'

##########
# CELERY #
##########
RABBITMQ_USER = environ.get('RABBITMQ_USER')
RABBITMQ_PASSWORD = environ.get('RABBITMQ_PASSWORD')
RABBITMQ_SERVER = environ.get('RABBITMQ_SERVER')
RABBITMQ_VHOST = environ.get('RABBITMQ_VHOST')
BROKER_URL = "amqp://{}:{}@{}/".format(
    RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_SERVER, RABBITMQ_VHOST
)


###########
# Storage #
###########

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = '/tmp'


###############################
# Weberservices configuration #
###############################

INFOCENTREWS_DESCRIPTION = 'https://rest-api-test2.u-strasbg.fr/infocentre/description.json'
INFOCENTREWS_BASE_URL = 'https://infocentrews-test.u-strasbg.fr'
