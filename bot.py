import pprint
from scholarly import scholarly
import csv
import tweepy
import datetime
import sys
import json

currentYear = datetime.datetime.now().year
api_keys_path = 'C:/Users/Colton/Github/BotComplexity/api_keys.json'

def create_api(api_keys_path):
    with open(api_keys_path) as f:
        api_keys = json.load(f)
        consumer_key = api_keys['consumer_key']
        consumer_secret = api_keys['consumer_secret']
        key = api_keys['key']
        secret = api_keys['secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e: 
        sys.exit('API verification failed')

    return api

def postTweet(tweet,api):
    api.update_status(tweet)
    
def composeTweet(authorName, authorHandles_dic, pubTitle, pub):
    pub = scholarly.fill(pub)
    pubURL = pub['pub_url']
    if 'pub_year' in pub['bib'].keys():
        if pub['bib']['pub_year'] == str(currentYear):
            if authorName in authorHandles_dic.keys():
                tweet = '[' + authorName + ']' + ' just published a new paper: "' + pubTitle + '"\n' + pubURL + '\n' + authorHandles_dic[authorName]
                return pubURL, tweet
            else:
                tweet = '[' + authorName + ']' + ' just published a new paper: "' + pubTitle + '"\n' + pubURL
                return pubURL, tweet
    return None, None
    
with open('C:/Users/Colton/Github/ScholarBot/authors.csv') as authorFile:
    authors = authorFile.readlines()
    lines = [item.strip() for item in authors]
    authorNames = []
    authorHandles_dic = {}
    for line in lines:
        if ',' in line and '@' in line:
            name = line[:line.find(',')]
            handle = line[line.find('@'):]
            authorNames.append(name)
            authorHandles_dic[name] = handle
        else:
            authorNames.append(line)

with open('C:/Users/Colton/Github/ScholarBot/pubs.csv') as pubFile:
    pubs = pubFile.readlines()
    pubIDs = [item.strip() for item in pubs]
    
newPubIDs = []
tweet_posted = False
api = create_api(api_keys_path)
for authorName in authorNames:
    search_query = scholarly.search_author(authorName)
    author = scholarly.fill(next(search_query))
    for pub in author['publications']:
        authPubID = pub['author_pub_id']
        iColon = authPubID.find(':')
        authID = authPubID[:iColon]
        pubID = authPubID[iColon+1:]
        pubTitle = pub['bib']['title']
        if not pubID in pubIDs:
            pubURL, tweet = composeTweet(authorName,authorHandles_dic, pubTitle, pub)
            if not tweet is None:
                postTweet(tweet,api)
                print(tweet)
                tweet_posted = True
            newPubIDs.append(pubID)

newPubIDs = list(dict.fromkeys(newPubIDs))
with open('C:/Users/Colton/Github/ScholarBot/pubs.csv','a') as pubFile:
    for pubID in newPubIDs:
        pubFile.write(pubID+'\n')

if tweet_posted == False:
	print('Nothing to tweet about today :/')
