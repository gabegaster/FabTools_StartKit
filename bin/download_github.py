#!/usr/bin/env python
"""This script is used to download all events from the github API
http://developer.github.com/v3/activity/events/
"""

# standard library
import os
import sys

# third party
from github import Github

# local
import utils

# authenticate to the API
config_parser = utils.get_config_parser()
if not config_parser.has_section('github'):
    sys.stderr.write(utils.yellow(
        "github is not configured; skipping...\n"
    ))
    exit(0)
api = Github(
    config_parser.get("github", "username"),
    config_parser.get("github", "password"),
)

# get all of the events for the authenticated user
user = api.get_user(config_parser.get("github", "username"))
for event in user.get_events():
    print event.created_at, event.type
    sys.stdout.flush()

sys.stderr.write(utils.green(
    "github complete!\n"
))
