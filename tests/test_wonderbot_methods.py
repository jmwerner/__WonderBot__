'''This script crawls a specified reddit and posts comments as the world
   renowned magician Tony Wonder'''

import sys
import os
import json
import praw
import pytest
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from wonderbot import WonderBot

## Tests ##

def test_submission_needs_reply(login_file_name, subreddit_name):
    reddit_bot = WonderBot(login_file=login_file_name, subreddit_name=subreddit_name)
    assert reddit_bot.submission_needs_reply("I wonder if this works")
    assert reddit_bot.submission_needs_reply("I wonder wonder wonder wonder if this works")
    assert reddit_bot.submission_needs_reply("I *wonder* if this works")
    assert reddit_bot.submission_needs_reply("I **wonder** if this works")
    assert reddit_bot.submission_needs_reply("I ~~wonder~~ if this works")
