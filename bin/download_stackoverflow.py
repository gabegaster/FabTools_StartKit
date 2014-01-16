#!/usr/bin/env python
"""This script is used to download all events from the stackoverflow API
http://developer.github.com/v3/activity/events/
"""

# standard library
import os
import sys
import datetime

# third party
import stackexchange

# local
import utils

# authenticate to the API
config_parser = utils.get_config_parser()
if not config_parser.has_section('stackoverflow'):
    sys.stderr.write(utils.yellow(
        "stackoverflow is not configured; skipping...\n"
    ))
    exit(0)

# authenticate. if this gives problems exceeding request limits,
# you'll need to obtain an API key
# https://github.com/lucjon/Py-StackExchange/tree/updating-2.0#api-keys
so = stackexchange.Site(stackexchange.StackOverflow)
so.impose_throttling = True

user = so.user(config_parser.get('stackoverflow', 'user_id'))
timeline = user.timeline.fetch()
# timeline = user.timeline.fetch( # i think this is the format
#     fromdate=datetime.datetime.now(),
#     todate=datetime.datetime.now()-datetime.timedelta(days=365),
# )
for event in timeline:
    date = datetime.datetime.fromtimestamp(event.json_ob.creation_date)
    detail = event.timeline_type
    if detail is None:
        detail = event.json_ob.post_type
    print date, detail
    sys.stdout.flush()

sys.stderr.write(utils.green(
    "stackoverflow complete for user %s!\n" % user.display_name
))
