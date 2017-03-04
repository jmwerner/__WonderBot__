'''This script crawls a specified reddit and posts comments as the world
   renowned magician Tony Wonder'''

import sys
import json
import praw
from pprint import pprint

LOGIN_FILE = 'login_info.json'


class WonderBot:
    '''This is the reddit bot class for handling all interaction with the web'''
    def __init__(self, login_file, subreddit_name):
        self.new_post_limit = 10
        self.bot_name = 'Tony Wonder'
        self.bot_account = '__WonderBot__'
        self.reply_text = 'Did somebody say... [Wonder?]' + \
                          '(http://imgur.com/a/wfYbY)'
        self.reddit = self.get_reddit_session(login_file)
        self.subreddit = self.get_subreddit_session(subreddit_name)

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

    def get_reddit_session(self, file):
        '''Authenticates and starts a praw.reddit.Reddit object
        Args:
            file (string): Path to file of authentication json
        Returns:
            praw.reddit.Reddit: Authenticated object
        '''
        login_info = self.read_json_from_file(file)
        reddit_object = praw.Reddit(client_id=login_info['client_id'],
                                    client_secret=login_info['secret'],
                                    redirect_uri='http://localhost:8080',
                                    user_agent=self.bot_name,
                                    username=login_info['username'], 
                                    password=login_info['password'])
        return reddit_object

    def get_subreddit_session(self, subreddit_name):
        '''Gets subreddit session
        Args:
            subreddit_name (string): Name of subreddit
        Returns:
            praw Subreddit object
        '''
        subreddit = self.reddit.subreddit(subreddit_name)
        return subreddit

    def get_new_posts(self):
        '''Returns new posts for specified subreddit
        Args:
            None
        Returns:
            Generator of new posts for subreddit
        '''
        newest_posts = self.subreddit.new(limit=self.new_post_limit)
        return newest_posts

    def get_comments_from_post(self, post_id):
        '''Returns all comments from post.
        Args:
            post_id (string): String of the post id.
        Returns:
            list: Comments from post
        '''
        post = self.reddit.submission(id=post_id)
        all_comments = post.comments.list()
        return all_comments


    def process_submission(self, submission):
        ''''''
        if 'wonder' in submission.title.lower().split() + \
                       submission.selftext.lower().split():
            # print('Replying to: {}'.format(submission.title))
            submission.reply(self.reply_text)
            # flat_comments = praw.helpers.flatten_tree(submission.comments)
            # print(flat_comments)

    @staticmethod
    def process_comment(submission):
        ''''''
        print(submission.body)
        print(submission.author)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        reddit_bot = WonderBot(login_file=LOGIN_FILE, subreddit_name='wondertest')
        if str(sys.argv[1]) == 'comments':
            print('comments')
        elif str(sys.argv[1]) == 'submissions':
            print('submissions')
        else:
            raise ValueError('Argument ' + str(sys.argv[1]) + ' not recognized')
    else:
        raise ValueError('Only 1 command line argument is supported')


    # for post in reddit_bot.subreddit.stream.submissions():
    #     process_submission(post)



# new_posts = reddit_bot.get_new_posts()



# comments = reddit_bot.get_comments_from_post(new_posts[0]['id'])


#         posts = list()
#         for submission in newest_posts:
#             post_dict = {"text": submission.selftext, "title": submission.title, \
#                          "id": submission.id, "subreddit_id": submission.subreddit_id}
#             posts.append(post_dict)





# [x.author == "Test" for x in all_comments]


