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


############
# Dipstrap #
############

DIPSTRAP_VERSION = '{{ dipstrap_version }}'
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION


################
# ADE settings #
################

ADE_WEB_API['USER'] = '{{ ade_ws_user }}'
ADE_WEB_API['PASSWORD'] = '{{ ade_ws_password }}'
ADE_WEB_API['HOST'] = '{{ ade_ws_host }}'

##########
# Sentry #
##########
sentry_init('test')
