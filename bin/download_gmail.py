#!/usr/bin/env python
"""Use this script to download a timeseries of emails sent from the GMail
API using the credentials specified in year-in-review.ini.
"""

# standard library
import os
import sys
import imaplib

# local
import utils

config_parser = utils.get_config_parser()
imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
imap_server.login(
    config_parser.get('google', 'email'),
    config_parser.get('google', 'password'),
)
print 'hi'
