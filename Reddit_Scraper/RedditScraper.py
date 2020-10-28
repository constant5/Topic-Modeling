import datetime as dt
import sys
import string
import traceback
import pandas as pd
import praw
from psaw import PushshiftAPI
import requests

class redditscraper():

    def __init__(self, credentials):
        
        # self.credentials = credentials
        Reddit = praw.Reddit(client_id=credentials['PERSONAL_USE_SCRIPT_14_CHARS'],
                        client_secret=credentials['SECRET_KEY_27_CHARS'],
                        user_agent=credentials['YOUR_APP_NAME'], 
                        username=credentials['YOUR_REDDIT_USER_NAME'], 
                        password=credentials['YOUR_REDDIT_LOGIN_PASSWORD'])
        self.ps_api = PushshiftAPI(Reddit)
        
    def __get_date__(self, created):
        return dt.datetime.fromtimestamp(created)


    def get_pushshift_data(self, topic, limit, after, sort, score):
        if isinstance(after, int): 
            after=int(dt.datetime(after, 1, 1).timestamp())
        return self.ps_api.search_comments(after=after,
                             subreddit=topic,
                             sort_type=score,
                             sort=sort,
                             limit=limit*10) # there is a bug in the psaw module that requires this multiplier

    def Get_Reddit_Comments(self, Sub_Reddit_Topic, Limit, how='top', after="5y"):

        try:
            if how == 'top':
                # posts = subreddit.top(limit=Limit)
                print(f'getting top {Limit} comments over last {after}')
                posts = self.get_pushshift_data(Sub_Reddit_Topic, Limit, after=after, sort='desc', score='score')
                # for p in posts: print(p.body)

            if how == 'asc':
                print(f'getting oldest {Limit} comments over last {after}')
                posts = self.get_pushshift_data(Sub_Reddit_Topic, Limit, after=after, sort='asc', score='created_utc')
            
            if how == 'desc':
                print(f'getting most recent {Limit} comments over last {after}')
                posts = self.get_pushshift_data(Sub_Reddit_Topic, Limit, after=after, sort='desc', score='created_utc')

            topics_dict = {"created": [], 
                           "body":[]}

            for submission in posts:
                if submission.body != '[removed]':
                    topics_dict["created"].append(submission.created)
                    topics_dict["body"].append(submission.body)
        
            topics_data = pd.DataFrame(topics_dict)
        
            _timestamp = topics_data["created"].apply(self.__get_date__)
        
            topics_data = topics_data.assign(timestamp = _timestamp)

            self.Access = 1

            return topics_data
        
        except Exception as e:

            print(e)

            error = 'invalid_grant error processing request'

            if error in "".join(traceback.format_exception(*sys.exc_info())):
                return error

            if "401" in str(e):

                return '\nWeb Access Error. received 401 HTTP response.\n'

            if "400" in str(e) or "403" in str(e)or "404" in str(e):

                 return str(e)
