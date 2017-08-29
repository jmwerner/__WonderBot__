'''This script crawls a specified reddit and posts comments as the world
   renowned magician Tony Wonder'''

import os
import json
import time
import praw
import re


class WonderBot:
    '''This is the reddit bot class for handling all interaction with the web'''
    def __init__(self, login_file, subreddit_name):
        self.login_file = login_file
        self.new_item_limit = 10
        self.bot_name = 'Tony Wonder'
        self.bot_account = '__WonderBot__'
        self.keyword = 'wonder'
        self.reply_text = 'Did somebody say... [Wonder?]' + \
                          '(http://i.imgur.com/figfAON.jpg)'
        self.reddit = self.get_reddit_session()
        self.subreddit = self.get_subreddit_session(subreddit_name)
        self.comments_log_name = 'logs/comments_log.txt'
        self.submissions_log_name = 'logs/submissions_log.txt'
        self.initialize_logs()

    @staticmethod
    def initialize_logs(directory='logs'):
        '''Initializes empty directory for log storing if it doesn't exist'''
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def read_json_from_file(file):
        '''Reads json from file and returns a dict.
        Args:
            file (string): Path to json file.
        Returns:
            dict: Read and parsed json.
        '''
        with open(file) as data_file:
            login_info = json.load(data_file)
        return login_info

    def get_reddit_session(self):
        '''Authenticates and starts a praw.reddit.Reddit object
        Returns:
            praw.reddit.Reddit: Authenticated object
        '''
        login_info = self.get_login_info()
        reddit_object = praw.Reddit(client_id=login_info['client_id'],
                                    client_secret=login_info['secret'],
                                    redirect_uri='http://localhost:8080',
                                    user_agent=self.bot_name,
                                    username=login_info['username'],
                                    password=login_info['password'])
        return reddit_object

    def get_login_info(self):
        '''Gets login info from login_file
        Returns:
            dict: secret info needed for praw login and reddit posting
        '''
        if os.path.isfile(self.login_file):
            return self.read_json_from_file(self.login_file)
        else:
            return {"client_id":os.environ["LOGIN_INFO_CLIENT_ID"],
                    "secret":os.environ["LOGIN_INFO_SECRET"],
                    "username":os.environ["LOGIN_INFO_USERNAME"],
                    "password":os.environ["LOGIN_INFO_PASSWORD"]}

    def get_subreddit_session(self, subreddit_name):
        '''Gets subreddit session.
        Args:
            subreddit_name (string): Name of subreddit.
        Returns:
            praw Subreddit object.
        '''
        subreddit = self.reddit.subreddit(subreddit_name)
        return subreddit

    def get_new_posts(self):
        '''Returns new posts for specified subreddit.
        Args:
            None
        Returns:
            Generator of new posts for subreddit.
        '''
        newest_posts = self.subreddit.new(limit=self.new_item_limit)
        return newest_posts

    def get_new_comments(self):
        '''Returns new posts for specified subreddit.
        Args:
            None
        Returns:
            Generator of new posts for subreddit.
        '''
        newest_posts = self.subreddit.comments(limit=self.new_item_limit)
        return newest_posts

    def get_comments_from_post(self, post_id):
        '''Returns all comments from post.
        Args:
            post_id (string): String of the post id.
        Returns:
            list: Comments from post.
        '''
        post = self.reddit.submission(id=post_id)
        all_comments = post.comments.list()
        return all_comments

    def submission_needs_reply(self, text):
        '''Determines if given text has the keyword within.
        Args:
            text (list): Text of post or comment.
        Returns:
            logical: True if self.keyword is within the text.
        '''
        punctuation = ('?', ':', '!', '.', ',', ';', '\'', '\"')
        stripped_string = ''.join(c for c in text if c not in punctuation)
        # Remove markdown characters
        words_list = stripped_string.lower().replace('*', '').replace('~~', '').split()
        # Remove mr from the front of a word split
        words_list = [re.sub(r'^{0}'.format(re.escape('mr')), '', x) for x in words_list]
        # Remove s from the end of a word split
        words_list = [re.sub(r's$', '', x) for x in words_list]
        return self.keyword in words_list

    def process_comment(self, comment):
        '''Processes and replies to a given comment if appropriate.
        Args:
            comment (object): Praw comment object.
        Returns:
            None
        '''
        if comment.author != self.bot_account:
            if self.submission_needs_reply(comment.body):
                if not self.id_in_log(comment.id, self.comments_log_name):
                    print('Replying to ' + comment.id)
                    self.write_to_log(comment.id, self.comments_log_name)
                    comment.reply(self.reply_text)

    def process_submission(self, submission):
        '''Processes and replies to a given submission if appropriate.
        Args:
            submission (object): Praw submission object.
        Returns:
            None
        '''
        if submission.author != self.bot_account:
            if self.submission_needs_reply(submission.selftext) or \
               self.submission_needs_reply(submission.title):
                if not self.id_in_log(submission.id, self.submissions_log_name):
                    print('Replying to ' + submission.id)
                    self.write_to_log(submission.id, self.submissions_log_name)
                    submission.reply(self.reply_text)

    def start_comment_batch(self):
        '''Processes and handles pre-set number of new comments'''
        for post in self.get_new_comments():
            self.process_comment(post)

    def start_submission_batch(self):
        '''Processes and handles pre-set number of new posts'''
        for submission in self.get_new_posts():
            self.process_submission(submission)

    @staticmethod
    def write_to_log(id_input, log_file_name):
        '''Writes given id to specified log file
        Args:
            id_input: id of post or comment
            log_file_name: file name of log to append
        Returns:
            None
        '''
        with open(log_file_name, 'a') as file:
            file.write(id_input + '\n')

    def id_in_log(self, id_input, log_file_name):
        '''Checks for given id in log
        Args:
            id_input: id of post or comment
            log_file_name: file name of log to read and check
        Returns:
            logical: True if id is already in log of ids, False otherwise
        '''
        try:
            ids = self.read_log(log_file_name)
            return id_input in ids
        except FileNotFoundError:
            return False

    @staticmethod
    def read_log(log_file_name):
        '''Reads log from file
        Args:
            log_file_name: file name of log to read
        Returns:
            list: Non-empty ids as strings retrieved from the log
        '''
        with open(log_file_name, 'r') as file:
            ids = file.read().split('\n')
            non_empty_ids = list(filter(None, ids))
        return non_empty_ids


def main():
    '''Main function that drives the comment and submission handling'''
    login_file = 'login_info.json'
    subreddit_name = 'arresteddevelopment'
    reddit_bot = WonderBot(login_file=login_file, subreddit_name=subreddit_name)
    reddit_bot.start_comment_batch()
    time.sleep(60)
    reddit_bot.start_submission_batch()

if __name__ == '__main__':
    main()
