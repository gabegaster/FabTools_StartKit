# 3rd party
from fabric.api import env, task, execute

# local
import utils
import provision

from fabtools.vagrant import vagrant

@task
def dev():
    """define development server"""
    env.provider = "virtualbox"
    utils.set_hosts_from_config()
    
    # TODO read the config.ini file here
    execute(vagrant, 'fab-tools-start-kit')
