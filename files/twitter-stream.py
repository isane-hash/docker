	
### **TWITTER STREAMING USING TWEEPY**

import tweepy
from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import textblob
import numpy as np
import pandas as pd
import re
from textblob import TextBlob
from textblob import Word




### **TWIITTER AUTHENTICATION KEY**

ACCESS_TOKEN = "1271910154347384833-SBpBowZFKyuOVwRlrsYziWx9wX71cW"
ACCESS_TOKEN_SECRET = "D3EPLvJJJik6jcwOqmnOB2VZtiiKWekp3LCZdCSiLpHv8"
CONSUMER_KEY = "1IR7mdNMrSC0rA8al8jrCNqzQ"
CONSUMER_SECRET = "KXLyvWquqmU7i6n0ik48SqZ6iXNxhpw9rKaC17uunLG1SbLHnd"

### **TWITTER CLIENT **

class TwitterClient():
    

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user
        

    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_hashtag(self, num_hashtags):
        home_timeline_tweets=[]
        for tweet in self.twitter_client.search(q=self.twitter_user, lang="en", rpp=num_hashtags):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
        
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        for tweet in self.twitter_client.search(q="Python", lang="en", rpp=10):
          print(f"{tweet.user.name}:{tweet.text}")
        friend_list = []
        # for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
        #     friend_list.append(friend)
        # return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


### **TWITTER AUTHENTICATER**

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth


### **TWITTER STREAMER**
#**Streaming and processing live tweets.**

class TwitterStreamer():
 
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)
        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)



### **TWITTER STREAM LISTENER**
#**This is a basic listener that prints received tweets to stdout.**


class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets):
        self.fetched_tweets = fetched_tweets

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)

#**Functionality for analyzing and categorizing content from tweets.**


class TweetAnalyzer():

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return ("Good")
        elif analysis.sentiment.polarity == 0:
            return ("Neutral")
        else:
            return ("Bad")
        
       

    def check_spelling(self, tweet):
      
      s= self.clean_tweet(tweet)
      # s = " Hello hyy gh"
      text = TextBlob(s)
      for word in s.split(' '):
        w = Word(word)
        w.spellcheck()

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
        df['check_spelling'] = np.array([tweet_analyzer.check_spelling(tweet) for tweet in df['tweets']])

        return df


if __name__ == '__main__':
    #  CODE TO STREAM LIVE TWEETS 
    # hash_tag_list = ["#covid-19", "#coronavirus"]
    # fetched_tweets_filename = "tweets.txt"
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

  
    ## search #covid-19
    home_timeline_tweets=[]
    for tweet in api.search(q="#coronavirus", lang="en", rpp=25):
        home_timeline_tweets.append(tweet)

    df = tweet_analyzer.tweets_to_data_frame(home_timeline_tweets)
    print("****CORONAVIRUS TWEETS****")
    print(df.head(15))

    # search #covid-19
    home_timeline_tweets=[]
    for tweet in api.search(q="#covid-19", lang="en", rpp=25):
        home_timeline_tweets.append(tweet)

    df = tweet_analyzer.tweets_to_data_frame(home_timeline_tweets)
    print("")
    print("****COVID-19 TWEETS****")
    print(df.head(15))