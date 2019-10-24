from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import re
import webbrowser
import pickle as pk
import pandas as pd
ckey='jeAKw9iLCh5Vu08tOmFdF4dy2'
csecret='By0zl0zKozpSyyTVrEt81XdhWz6edM5feI4GE7Kx5UegzCtK99'
atoken='998423444541747200-SxbaEMS2HnOFOCIS6hx3j7bRxBUgUT6'
asecret='xdIjOGOcKfG99dTTwPMNCM1NgfocXZ1pZjsFfijILVznW'

tweets=[]
class live_listener(StreamListener):
    def on_data(self, data):
        data=json.loads(data)

        if(data["lang"] == "en"):
            tweets.append(data["text"])


    def on_error(self, status):
        print(status)

def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
with open('./model/mlp_classifier.pkl', 'rb') as fid:
    model = pk.load(fid)

with open('./model/TFIDF_vector.pkl', 'rb') as file:
    tfidf = pk.load(file)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener=live_listener())
query=input("Enter the query you want to track: ")
twitterStream.filter(track=[query], is_async=True)
time.sleep(15)
twitterStream.disconnect()
cleaned_tweets=[]
for tweet in tweets:
    cleaned_tweet = clean_tweet(tweet)
    cleaned_tweets.append(cleaned_tweet)

df = pd.DataFrame({'cleaned_tweets':cleaned_tweets})

# load model
with open('./model/mlp_classifier.pkl', 'rb') as fid:
    model = pk.load(fid)
with open('./model/TFIDF_vector.pkl', 'rb') as file:
    tfidf = pk.load(file)

comment_vectorised = tfidf.transform(cleaned_tweets)
df['Sentiment'] = model.predict(comment_vectorised)
df['Sentiment'] = df['Sentiment'].map({0: 'positive', 1: 'neutral', 2: 'negative'})
sentiment = df['Sentiment']
print("Prediction done.")

print(df)