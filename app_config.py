#!/usr/bin/env python

"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
See get_secrets() below for a fast way to access them.
"""

import os

"""
NAMES
"""
# Project name used for display
PROJECT_NAME = 'Lobbying Missouri'

# Use dashes, not underscores!
#PROJECT_SLUG = 'stl-lobbying'

# The name of the repository containing the source
REPOSITORY_NAME = 'stl-lobbying'
REPOSITORY_URL = 'git@github.com:nprapps/%s.git' % REPOSITORY_NAME
REPOSITORY_ALT_URL = None # 'git@bitbucket.org:nprapps/%s.git' % REPOSITORY_NAME'

# The name to be used in paths on the server
PROJECT_FILENAME = 'stl_lobbying'

"""
DEPLOYMENT
"""
PRODUCTION_S3_BUCKETS = ['www.lobbyingmissouri.org']
STAGING_S3_BUCKETS = ['staging.lobbyingmissouri.org']

PRODUCTION_SERVERS = ['cron.nprapps.org']
STAGING_SERVERS = ['50.112.92.131']

# Should code be deployed to the web/cron servers?
DEPLOY_TO_SERVERS = True 

SERVER_USER = 'ubuntu'
SERVER_PYTHON = 'python2.7'
SERVER_PROJECT_PATH = '/home/%s/apps/%s' % (SERVER_USER, PROJECT_FILENAME)
SERVER_REPOSITORY_PATH = '%s/repository' % SERVER_PROJECT_PATH
SERVER_VIRTUALENV_PATH = '%s/virtualenv' % SERVER_PROJECT_PATH

# Should the crontab file be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_CRONTAB = True

# Should the service configurations be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_SERVICES = False

UWSGI_SOCKET_PATH = '/tmp/%s.uwsgi.sock' % PROJECT_FILENAME
UWSGI_LOG_PATH = '/var/log/%s.uwsgi.log' % PROJECT_FILENAME
APP_LOG_PATH = '/var/log/%s.app.log' % PROJECT_FILENAME

# Services are the server-side services we want to enable and configure.
# A three-tuple following this format:
# (service name, service deployment path, service config file extension)
SERVER_SERVICES = [
    ('app', SERVER_REPOSITORY_PATH, 'ini'),
    ('uwsgi', '/etc/init', 'conf'),
    ('nginx', '/etc/nginx/locations-enabled', 'conf'),
]

# These variables will be set at runtime. See configure_targets() below
S3_BUCKETS = []
S3_BASE_URL = ''
SERVERS = []
SERVER_BASE_URL = ''
DEBUG = True

"""
COPY EDITING
"""
COPY_GOOGLE_DOC_KEY = '0AlXMOHKxzQVRdG45Ti1TYkNSOWR1cDI2V0x6WUt6S3c'
ORGANIZATION_NAME_LOOKUP_DOC_KEY = '0AlXMOHKxzQVRdFJNMlZTXy1pSFNRUHJIR3RVSWhJSGc'
LEGISLATOR_DEMOGRAPHICS_DOC_KEY = '0AlXMOHKxzQVRdFFQRzBuLUxhN0JubjlvRVA2SlpVVlE'

"""
SHARING
"""
PROJECT_DESCRIPTION = 'Tracking lobbyist gifts to Missouri lawmakers. How much did yours accept? #MoLeg via @stlpublicradio and @npr'
SHARE_URL = 'http://www.lobbyingmissouri.org/'

TWITTER = {
    'TEXT': '%s' % PROJECT_DESCRIPTION,
    'URL': SHARE_URL,
    # Will be resized to 120x120, can't be larger than 1MB 
    'IMAGE_URL': 'http://www.lobbyingmissouri.org/img/promo.png'
}

FACEBOOK = {
    'TITLE': PROJECT_NAME,
    'URL': SHARE_URL,
    'DESCRIPTION': PROJECT_DESCRIPTION,
    # Should be square. No documented restrictions on size
    'IMAGE_URL': TWITTER['IMAGE_URL']
}

GOOGLE = {
    # Thumbnail image for Google News / Search.
    # No documented restrictions on resolution or size
    'IMAGE_URL': TWITTER['IMAGE_URL']
}

"""
SERVICES
"""
SLPR_GOOGLE_ANALYTICS_ID = 'UA-45354605-1'
OUR_GOOGLE_ANALYTICS_ID = 'UA-5828686-58'

"""
Utilities
"""
def get_secrets():
    """
    A method for accessing our secrets.
    """
    secrets = [
        'EXAMPLE_SECRET'
    ]

    secrets_dict = {}

    for secret in secrets:
        name = '%s_%s' % (PROJECT_FILENAME, secret)
        secrets_dict[secret] = os.environ.get(name, None)

    return secrets_dict

def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKETS
    global S3_BASE_URL
    global SERVERS
    global SERVER_BASE_URL
    global DEBUG
    global DEPLOYMENT_TARGET

    if deployment_target == 'production':
        S3_BUCKETS = PRODUCTION_S3_BUCKETS
        S3_BASE_URL = 'http://www.lobbyingmissouri.org'
        SERVERS = PRODUCTION_SERVERS
        SERVER_BASE_URL = 'http://%s' % (SERVERS[0])
        DEBUG = False
    elif deployment_target == 'staging':
        S3_BUCKETS = STAGING_S3_BUCKETS
        S3_BASE_URL = 'http://staging.lobbyingmissouri.org'
        SERVERS = STAGING_SERVERS
        SERVER_BASE_URL = 'http://%s' % (SERVERS[0])
        DEBUG = True
    else:
        S3_BUCKETS = [] 
        S3_BASE_URL = 'http://127.0.0.1:8000'
        SERVERS = []
        SERVER_BASE_URL = 'http://127.0.0.1:8001'
        DEBUG = True

    DEPLOYMENT_TARGET = deployment_target

"""
Run automated configuration
"""
DEPLOYMENT_TARGET = os.environ.get('DEPLOYMENT_TARGET', None)

configure_targets(DEPLOYMENT_TARGET)

