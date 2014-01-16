#!/usr/bin/env python
"""Use this script to download a timeseries of tweets from the Twitter
API using the credentials specified in year-in-review.ini.
"""

# standard library
import os
import sys

# third party
import tweepy

# local
import utils

def authenticate(config_parser):

    if not config_parser.has_section('twitter'):
        sys.stderr.write(utils.yellow(
            "twitter is not configured; skipping...\n"
        ))
        exit(0)

    # The consumer keys can be found on your application's Details
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    consumer_key = config_parser.get('twitter', 'consumer_key')
    consumer_secret = config_parser.get('twitter', 'consumer_secret')

    # The access tokens can be found on your applications's Details
    # page located at https://dev.twitter.com/apps (located 
    # under "Your access token")
    access_token = config_parser.get('twitter', 'access_token')
    access_token_secret = config_parser.get('twitter', 'access_token_secret')
    
    # authenticate and use the api object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

# If the authentication was successful, you should
# see the name of the account print out
api = authenticate(utils.get_config_parser())

# print out the tweet timestamps and some basic statistics about those
# tweets
for status in tweepy.Cursor(api.user_timeline).items():
    print status.created_at, status.retweet_count, status.favorite_count

sys.stderr.write(utils.green(
    "twitter complete!\n"
))
