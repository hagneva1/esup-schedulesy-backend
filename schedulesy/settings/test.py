# -*- coding: utf-8 -*-

from os.path import normpath
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

DATABASES['default']['HOST'] = '{{ default_db_host }}'
DATABASES['default']['USER'] = '{{ default_db_user }}'
DATABASES['default']['PASSWORD'] = '{{ default_db_password }}'
DATABASES['default']['NAME'] = '{{ default_db_name }}'

DATABASES['ade']['HOST'] = '{{ ade_db_host}}'
DATABASES['ade']['USER'] = '{{ ade_db_user }}'
DATABASES['ade']['PASSWORD'] = '{{ ade_db_password }}'
DATABASES['ade']['NAME'] = '{{ ade_db_name }}'


############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '.u-strasbg.fr',
    '.unistra.fr',
]

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = '{{ remote_current_path }}/log/app.log'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


################
# ADE settings #
################

ADE_WEB_API['USER'] = '{{ ade_ws_user }}'
ADE_WEB_API['PASSWORD'] = '{{ ade_ws_password }}'
ADE_WEB_API['HOST'] = '{{ ade_ws_host }}'
ADE_WEB_API['PROJECT_ID'] = '{{ ade_ws_project_id }}'

#########
# STAGE #
#########

STAGE = '{{ goal }}'

##########
# Sentry #
##########
sentry_init(STAGE)


######
# S3 #
######

AWS_ACCESS_KEY_ID = '{{ s3_access_key }}'
AWS_SECRET_ACCESS_KEY = '{{ s3_secret_key }}'
AWS_STORAGE_BUCKET_NAME = 'schedulesy_test'

##########
# CELERY #
##########
RABBITMQ_USER = '{{ rabbitmq_user }}'
RABBITMQ_PASSWORD = '{{ rabbitmq_password }}'
RABBITMQ_SERVER = '{{ rabbitmq_server }}'
RABBITMQ_VHOST = '{{ rabbitmq_vhost }}'
BROKER_URL = "amqp://{}:{}@{}/".format(
    RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_SERVER, RABBITMQ_VHOST
)
