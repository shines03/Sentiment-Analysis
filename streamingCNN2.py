from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import re
import pickle as pk
import pandas as pd
ckey1='YtxaH4JWVc3zAjLkcRLYRX1jq'
csecret1='Xdv1GID3ae3sQAoFNSHVOmAJXr0Lsg90wXJOVF4dvT32xJaCp2'
atoken1='837744358652841984-tu9CUFPIECE7LHoIxkzy0OL0mXC45GS'
asecret1='EMn9cN9PKmQHv3xCbXagsTmOQiFHg2mZGcvNkJl8XKN0Y'

ckey2 = "Up9TAIibITwyeZx1sk6J0MnzA"
csecret2 = "xHes49T865z5XUAWPhm1ST2Oal5Jz2rLFJqkyzJFtgw5FF5c49"
atoken2 = "837744358652841984-RNB7NtUl3a29cqxuQ6ixreYhnY04Zyi"
asecret2 = "nImSBMzzYcatWFPpD182BnPBO9eFkqUl8lrHEsTCi6ceq"

tweets1=[]

class live_listener1(StreamListener):
    def on_data(self, data):
        data=json.loads(data)

        if(data["lang"] == "en"):
            tweets1.append(data["text"])


    def on_error(self, status):
        print(status)

tweets2=[]

class live_listener2(StreamListener):
    def on_data(self, data):
        data=json.loads(data)

        if(data["lang"] == "en"):
            tweets2.append(data["text"])


    def on_error(self, status):
        print(status)

def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
with open('./model/mlp_classifier.pkl', 'rb') as fid:
    model = pk.load(fid)

with open('./model/TFIDF_vector.pkl', 'rb') as file:
    tfidf = pk.load(file)


auth1 = OAuthHandler(ckey1, csecret1)
auth1.set_access_token(atoken1, asecret1)
twitterStream1 = Stream(auth1, listener=live_listener1())
query1=input("Enter the query you want to track: ")
twitterStream1.filter(track=[query1], is_async=True)

auth2 = OAuthHandler(ckey2, csecret2)
auth2.set_access_token(atoken2, asecret2)
twitterStream2 = Stream(auth2, listener=live_listener2())
query2=input("Enter the query you want to track: ")
twitterStream2.filter(track=[query2], is_async=True)

time.sleep(40)

twitterStream1.disconnect()
twitterStream2.disconnect()

cleaned_tweets1=[]
cleaned_tweets2=[]
for tweet in tweets1:
    cleaned_tweet = clean_tweet(tweet)
    cleaned_tweets1.append(cleaned_tweet)
for tweet in tweets2:
    cleaned_tweet = clean_tweet(tweet)
    cleaned_tweets2.append(cleaned_tweet)

df1 = pd.DataFrame({'cleaned_tweets':cleaned_tweets1})
df2 = pd.DataFrame({'cleaned_tweets':cleaned_tweets2})

# load model
with open('./model/mlp_classifier.pkl', 'rb') as fid:
    model = pk.load(fid)
with open('./model/TFIDF_vector.pkl', 'rb') as file:
    tfidf = pk.load(file)

comment_vectorised = tfidf.transform(cleaned_tweets1)
df1['Sentiment'] = model.predict(comment_vectorised)
df1['Sentiment'] = df1['Sentiment'].map({0: 'positive', 1: 'neutral', 2: 'negative'})
print("Prediction done.")

comment_vectorised = tfidf.transform(cleaned_tweets2)
df2['Sentiment'] = model.predict(comment_vectorised)
df2['Sentiment'] = df2['Sentiment'].map({0: 'positive', 1: 'neutral', 2: 'negative'})
print("Prediction done.")

print(df1)
print(df2)