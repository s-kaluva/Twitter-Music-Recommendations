import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json
from pprint import pprint
from statistics import mean
 
consumer_key = 'uIBOtkATV7Whq0SQ7ysSAbeLG'
consumer_secret = 'n19i6ZpD2jDMfmO3iaxMU2vtofUk9rODWoLmySugpWMEChXUH9'
access_token = '163000023-vuXUE4JVw4RtBvHJqDD5hP7Ov66xbboUhOvqtaoS'
access_token_secret = 'ncwb0hZ9KHa0IYFKIWrXUDt4RnxGVz1RcyMrz5O2hctXi'

# Function to extract tweets 
def get_tweets(username): 
          
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_token, access_token_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
  
        # 200 tweets to be extracted 
        number_of_tweets=10
        tweets = api.user_timeline(screen_name=username) 
  
        # Empty Array 
        tmp=[]  
  
        # create array of tweet information: username,  
        # tweet id, date/time, text 
        tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  
        for j in tweets_for_csv: 
            cleaned=clean_text(j)
            score=analize_sentiment(cleaned)

            tmp.append(score)
        return mean(tmp)

def clean_text(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

def analize_sentiment_pol(text):
    analysis = TextBlob(text)
    return analysis.sentiment.subjectivity

# reading json file
def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def music_sent_score(lyric):
    scoreList=[]
    

if __name__ == '__main__':
    jsonData = read_file('tracks.json')
    tweet_mean_score = get_tweets("realDonaldTrump")
#     print (tweet_mean_score)
    songs = {}
    cleanLyrics = ''
    mag=9
    finalsong={}
    for i in range(len(jsonData)):
        new_mag=0
        songs[i]=jsonData[i]
#         print (songs)
        songs[i]['lyrics']=clean_text(songs[i]['lyrics'])
        songs[i]['score']=analize_sentiment_pol(songs[i]['lyrics'])
        new_mag = abs(float(songs[i]['score']) - float(tweet_mean_score))
#         print (float(new_mag))
#         if(new_mag < mag):
#             print ("test")
        finalsong[new_mag]=songs[i]
#             mag=new_mag
#     print (songs)
#     sorted(finalsong)
    sorted_list = list()
    for keys in sorted(finalsong):
        sorted_list.append(finalsong[keys])
    for i in range(len(sorted_list)):
        print ('Song:',sorted_list[i]['name'],'--- By:',sorted_list[i]['artist'],'\n')
