# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 20:36:39 2018

@author: Shines03
"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


ckey='YtxaH4JWVc3zAjLkcRLYRX1jq'
csecret='Xdv1GID3ae3sQAoFNSHVOmAJXr0Lsg90wXJOVF4dvT32xJaCp2'
atoken='837744358652841984-YD9AjJAI3NfbmScfhWkpsskEZb4Vc07'
asecret='DnGNCv3VlvhD6iDUCHzwr3TvNK4AqTqYKA5refo4hIGiy'

file_counter = 0

class live_listener(StreamListener):
    def on_data(self, data):
        data=json.loads(data)

        global file_counter

        if(data["lang"]=="en"):
            print(data["text"])

            tweet_dict = {"created_at":data["created_at"],
                          "tweet": data["text"],
                          "username": data["user"]["name"],
                          "location": data["user"]["location"]}
            filename = "tweets_{:d}.json".format(file_counter)
            with open('./tweets/'+filename, 'w+') as f:
                f.write(json.dumps(tweet_dict))
            file_counter += 1
        return data

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener=live_listener())
twitterStream.filter(track=["oneplus"])