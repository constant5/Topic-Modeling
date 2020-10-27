import datetime as dt
import sys
import string
import traceback
import pandas as pd
import praw

import requests

class redditscraper():

    def __init__(self, credentials):
        
        self.credentials = credentials

    def __get_date__(self, created):
        return dt.datetime.fromtimestamp(created)

    def get_pushshift_data(self, data_type, **kwargs):
        """
        Gets data from the pushshift api.

        data_type can be 'comment' or 'submission'
        The rest of the args are interpreted as payload.

        Read more: https://github.com/pushshift/api
        """

        base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
        payload = kwargs
        request = requests.get(base_url, params=payload)
        # print(f'payload for {request.url}')
        data = pd.DataFrame.from_records(request.json().get('data'), columns=['author_created_utc','title'])
        data.rename(columns= {'author_created_utc':'created'} , inplace=True)
        data = data[data['created']>0]
        return  data

    def ps_args(self, data_type="submission", duration="30d" , size=1000 , sort_type="created_utc", sort="asc", subreddit='Sports' ):
        args = {
                'data_type':data_type,       # give me "comments" or "submission" to publish something
                'duration':duration,         # Select the timeframe. Epoch value or Integer + "s,m,h,d" (i.e. "second", "minute", "hour", "day")
                'size':size,                 # maximum 1000 comments
                'sort_type':sort_type,       # Sort by score (Accepted: "score", "num_comments", "created_utc")
                'sort':sort,                 # sort by asc or desc
                'subreddit':subreddit,       #"author", "link_id", "created_utc", "subreddit"
                }
        return args

    def Get_Reddit_Comments(self, Sub_Reddit_Topic, Limit, how='top', duration="10d"):

        YOUR_APP_NAME                = self.credentials['YOUR_APP_NAME']
        PERSONAL_USE_SCRIPT_14_CHARS = self.credentials['PERSONAL_USE_SCRIPT_14_CHARS']
        SECRET_KEY_27_CHARS          = self.credentials['SECRET_KEY_27_CHARS']
        YOUR_REDDIT_USER_NAME        = self.credentials['YOUR_REDDIT_USER_NAME']
        YOUR_REDDIT_LOGIN_PASSWORD   = self.credentials['YOUR_REDDIT_LOGIN_PASSWORD']

        try:

            # Getting a Reddit instance
            Reddit = praw.Reddit(client_id=PERSONAL_USE_SCRIPT_14_CHARS,
                                 client_secret=SECRET_KEY_27_CHARS,
                                 user_agent=YOUR_APP_NAME, 
                                 username=YOUR_REDDIT_USER_NAME, 
                                 password=YOUR_REDDIT_LOGIN_PASSWORD)

            # Getting a Sub Reddit instance
            subreddit = Reddit.subreddit(Sub_Reddit_Topic)

            # Let’s just grab the most up-voted topics all-time with:
            # be aware that Reddit’s request limit* is 1000
            if how == 'top':
                posts = subreddit.top(limit=Limit)

                topics_dict = { "title":[], 
                                # "score":[], 
                                # "id":[], "url":[], 
                                # "comms_num": [], 
                                "created": [], 
                                "body":[]}

                for submission in posts:
                    topics_dict["title"].append(submission.title)
                    # topics_dict["score"].append(submission.score)
                    # topics_dict["id"].append(submission.id)
                    # topics_dict["url"].append(submission.url)
                    # topics_dict["comms_num"].append(submission.num_comments)
                    topics_dict["created"].append(submission.created)
                    topics_dict["body"].append(submission.selftext)
            
                topics_data = pd.DataFrame(topics_dict)
                # print(topics_data.head())

            elif how == 'asc':
                kwargs = self.ps_args(sort='asc', subreddit=Sub_Reddit_Topic, size=Limit, duration="10d")
                topics_data = self.get_pushshift_data(**kwargs)
                # print(topics_data[['created', 'title']].head())
            elif how == 'desc':
                kwargs = self.ps_args(sort='desc', subreddit=Sub_Reddit_Topic, size=Limit, duration="10d")
                topics_data = self.get_pushshift_data(**kwargs)
                # print(topics_data[['created', 'title']].head())


        
            _timestamp = topics_data["created"].apply(self.__get_date__)
        
            topics_data = topics_data.assign(timestamp = _timestamp)
            # print(topics_data.head())
        
            # topics_data.to_csv('Sub_Reddit_Topics.csv', index=False)

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
