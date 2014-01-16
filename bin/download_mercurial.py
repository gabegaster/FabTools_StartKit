#!/usr/bin/env python
"""Use this script to download a timeseries of mercurial commits on
arbitrary machines using the credentials specified in
year-in-review.ini. This script currently only extracts the timeseries
for parent repositories, not for subrepositories!
"""

# standard library
import ConfigParser
import sys

# third party
from fabric.api import *

# local
import utils

# get the necessary information from the config parser
config_parser = utils.get_config_parser()
if not config_parser.has_section('mercurial'):
    sys.stderr.write(utils.yellow(
        "mercurial is not configured; skipping...\n"
    ))
    exit(0)
email = config_parser.get('mercurial', 'email')
host_directories = config_parser.get('mercurial', 'host_directories')

# configure fabric to use ssh configuration
# http://docs.fabfile.org/en/latest/usage/execution.html#leveraging-native-ssh-config-files
env.use_ssh_config = True
env.ssh_config_path = config_parser.get('mercurial', 'ssh_config_path')

# iterate over all comma-separated 'host:directory' pairs
for host_directory in host_directories.split(','):
    host, directory = host_directory.strip().split(':')
    host = host.strip()
    directory = directory.strip()

    # Find all subdirectories that contain mercurial roots (.hg/)
    # directories. This traverses the directory tree recursively, so
    # subrepos will always be listed *after* their parent repositories
    vcs_dir = '.hg'
    with settings(hide('commands'), host_string=host):
        repo_roots = run("find %s -type d -name '%s'" % (directory, vcs_dir))

        # Extract commit history from these mercurial root directories that
        # correspond with the specified user email
        last_nonsubrepo_repo_root = None
        for repo_root in repo_roots.splitlines():
            repo_root = repo_root.replace(vcs_dir, '')

            # print some updates
            host_repo = ':'.join([host, repo_root])
            sys.stderr.write(utils.green(
                'examining hg repo at %s\n' % host_repo
            ))

            # check to see if this repo is actually a
            # subrepository. only need to check the last
            # nonsubrepo_repo_root because of how `find` recursively
            # traverses the directory tree
            is_subrepo = False
            if (last_nonsubrepo_repo_root 
                and repo_root.startswith(last_nonsubrepo_repo_root)):
                is_subrepo = True

            # only extract the timestamps for non-subrepositories
            if not is_subrepo:
                last_nonsubrepo_repo_root = repo_root
                with cd(repo_root):
                    timestamps = run(
                        "hg log -u %s --template '{date|isodate}\n'" % email
                    )
                    for timestamp in timestamps.splitlines():
                        t = ' '.join(timestamp.split()[:2])
                        print t, host_repo
                    sys.stdout.flush()
