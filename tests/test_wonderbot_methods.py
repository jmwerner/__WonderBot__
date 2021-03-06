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
    assert reddit_bot.submission_needs_reply("I WONDER if this works")
    assert reddit_bot.submission_needs_reply("I wonder wonder wonder wonder if this works")
    assert reddit_bot.submission_needs_reply("I *wonder* if this works")
    assert reddit_bot.submission_needs_reply("I **wonder** if this works")
    assert reddit_bot.submission_needs_reply("I ~~wonder~~ if this works")
    assert reddit_bot.submission_needs_reply("*wonder* if this works")
    assert reddit_bot.submission_needs_reply("I this works **wonder**")
    assert reddit_bot.submission_needs_reply("~~wonder~~ if this works")
    assert reddit_bot.submission_needs_reply("Mr.Wonder is my hero")
    assert reddit_bot.submission_needs_reply("I dig Mr.Wonder, he is my hero")
    assert reddit_bot.submission_needs_reply("I dig Mr.Wonder he is my hero")
    assert reddit_bot.submission_needs_reply("I dig Wonder's, he is my hero")
    assert reddit_bot.submission_needs_reply("I dig Wonder's he is my hero")
    assert reddit_bot.submission_needs_reply("I dig Mr.Wonder, he wonder is my hero")
    assert reddit_bot.submission_needs_reply("I dig Mr.Wonder he is my WONDER hero")
    assert reddit_bot.submission_needs_reply("I dig Wonder's, he is my wonder hero")
    assert reddit_bot.submission_needs_reply("I dig Wonder's he is my wonder hero")
    assert reddit_bot.submission_needs_reply("He is amazing, he can work wonders")
