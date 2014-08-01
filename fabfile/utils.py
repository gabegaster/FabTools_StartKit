# standard library
import os
import ConfigParser

# 3rd party
import requests
from fabric.api import *
from fabric import colors
import fabtools

# local
import exceptions

def fabfile_root():
    return os.path.dirname(os.path.abspath(__file__))

def fabfile_templates_root():
    return os.path.join(fabfile_root(), "templates")

def project_root():
    return os.path.dirname(fabfile_root())

def remote_project_root():
    return "/vagrant"

def get_config_parser():
    parser = ConfigParser.RawConfigParser()
    parser.read(os.path.join(project_root(), "config.ini"))
    return parser

def set_hosts_from_config():
    parser = get_config_parser()
    env.hosts = parser.get('servers', env.provider).split(",")

def set_timezone(timezone):
    run_as_root('echo "%s" > /etc/timezone' % timezone)
    run_as_root('dpkg-reconfigure --frontend noninteractive tzdata')
    require.service.restarted('cron')

def require_timezone(timezone):
    with settings(hide('commands'), warn_only=True):
        result = run('grep -q "^%s$" /etc/timezone' % timezone)
        ret_code = result.return_code
    if ret_code == 0:
        return
    elif ret_code == 1:
        set_timezone(timezone)
    else:
        raise SystemExit()

