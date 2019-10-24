# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 18:02:22 2018

@author: Shines03
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 20:36:39 2018

@author: Shines03
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import re
from textblob import TextBlob
import webbrowser

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

def get_tweet_sentiment(tweet): 
        analysis = TextBlob(tweet) 
        if analysis.sentiment.polarity > 0: 
            return 'POSITIVE'
        elif analysis.sentiment.polarity == 0: 
            return 'NEUTRAL'
        else: 
            return 'NEGATIVE'
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener=live_listener())
query=input("Enter the query you want to track: ")
twitterStream.filter(track=[query], async=True)
time.sleep(30)
twitterStream.disconnect()
result=[]
total_tweets=0
ptweets=0
ntweets=0
nutweets=0
for tweet in tweets:
    item={}
    cleaned_tweet=clean_tweet(tweet)
    item['clean_tweet']=cleaned_tweet
    item['sentiment']=get_tweet_sentiment(cleaned_tweet)
    total_tweets+=1
    if item['sentiment']=="POSITIVE":
        ptweets+=1
    elif item['sentiment']=="NEGATIVE":
        ntweets+=1
    else:
        nutweets+=1
    result.append(item)
ptweets=str(round((ptweets*100/total_tweets),2))
ntweets=str(round((ntweets*100/total_tweets),2))
nutweets=str(round((nutweets*100/total_tweets),2))
total_tweets=str(total_tweets)

htmlString1 = """

<html>
    <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    </head>
    <body>
        <div style="padding:15px;">
            <div style="text-align:center; padding:10px; background-color:#003cb3; border:1px white solid; border-radius:25px; color:white; "><h1 style="color:white;">Final Sentiment Scores</h1></div>
            <br>
            <div><h2 style="text-align:center;">Total tweets collected: """+total_tweets+"""</h2></div>
        </div>
        <div class="row">
            <div class="col" style="text-align:center;">
                <img src="green.jpg" alt="Smiley face" height="300" width="300"></img>
                <h3>Positive Sentiments: """+ptweets+"""</h3>
            </div>
            <div class="col" style="text-align:center;">
                <img src="yellow.jpg" alt="Smiley face" height="300" width="300"></img>
                <h2>Neutral Sentiments: """+nutweets+"""</h2>
            </div>
            <div class="col" style="text-align:center;">
                <img src="red.jpg" alt="Smiley face" height="300" width="300"></img>
                <h2>Negative Sentiments: """+ntweets+"""</h2>
            </div>
        </div>
        """
htmlString2 = """ <br><br><div><h2 style="text-align:center;">Tweets over Analysis has been done</h2></div>
                <div style="padding:20px">"""
for item in result:
    htmlString2 += """
        <div class="row" style="margin:5px; background: -webkit-radial-gradient(10% 30%, #3366ff, #99b3ff); border:1px black solid; border-radius:2px; font-size:14px; font-weight:bold; font-family:tahoma; padding:10px;">
            <div class="col-md-10 col-sm-12">"""+item['clean_tweet']+"""</div>
            <div class="col-md-2 col-sm-12" style="text-align:right;">"""+item['sentiment']+"""</div>
        </div>"""
htmlString3 = """
        </div>
    </body>

</html>

"""
htmlString = htmlString1+htmlString2+htmlString3
view = open('view.html','w', encoding="UTF-8")
view.write(htmlString)
view.close()
filename = 'view.html'
webbrowser.open_new_tab(filename)