import requests
import re
import pickle as pk
import pandas as pd
from langdetect import detect
token = 'EAACW5Fg5N2IBAH8rRkhwIFCZCKSnafd1PrV9pqZCLxeOhkqKlZAXxbz4HXUxxZBZCKFzMIspdqMTzCqrVKx9u3q10CZAOZAweOfrpUTEaUZBrOGy8iWh5kce7qjt1URs07fVXayHZAQa3LZCJr0TrLqRxbdAodVVuZAFSVFvuEhZC306NQZDZD'
page_name = input('Enter the page_name: ')
req = page_name+'?fields=posts.limit(100){message,comments.limit(100){message}}'
def req_facebook(req):
    r= requests.get('https://graph.facebook.com/v3.0/'+req, {'access_token':token})
    return r
results = req_facebook(req).json()
num_of_posts = int(input("Enter the number of posts: "))
comments=[]
for i in range(0,num_of_posts):
    try:
        if 'comments' in results['posts']['data'][i].keys():
            for j in range(0, len(results['posts']['data'][i]['comments']['data'])):
                if 'message' in results['posts']['data'][i]['comments']['data'][j].keys():
                    cmnt = results['posts']['data'][i]['comments']['data'][j]['message']
                    try:
                        if detect(cmnt) == 'en':
                            comments.append(cmnt)
                    except:
                        pass
    finally:
        pass


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())


cleaned_comments=[]

for comment in comments:
    cleaned_comments.append(clean_tweet(comment))

df = pd.DataFrame({'cleaned_comments':cleaned_comments})

# load model
with open('./model/mlp_classifier.pkl', 'rb') as fid:
    model = pk.load(fid)
with open('./model/TFIDF_vector.pkl', 'rb') as file:
    tfidf = pk.load(file)

comment_vectorised = tfidf.transform(cleaned_comments)
df['Sentiment'] = model.predict(comment_vectorised)
df['Sentiment'] = df['Sentiment'].map({0: 'positive', 1: 'neutral', 2: 'negative'})


dic={}

for i in range(0,len(df['Sentiment'])):
    dic[df['cleaned_comments'][i]]=df['Sentiment'][i]

print(dic)