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


## Helper Functions ##

def comment_was_handled_correctly(comment, bot):
    if comment.author != bot.bot_account:
        if bot.submission_needs_reply(comment.body):
            all_comments = comment.replies.list()
            all_authors = [x.author for x in all_comments]
            if bot.bot_account in all_authors:
                return True
            else:
                return False
        else:
            return True
    else:
        return True


## Tests ##

def test_newest_comments(login_file_name, subreddit_name):
    reddit_bot = WonderBot(login_file=login_file_name, subreddit_name=subreddit_name)
    comments = reddit_bot.get_new_comments()
    for comment in comments:
        assert comment_was_handled_correctly(comment, reddit_bot)

