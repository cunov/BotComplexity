import pprint
from scholarly import scholarly
import csv
import tweepy
import datetime
import sys

currentYear = datetime.datetime.now().year

def create_api():
    auth = tweepy.OAuthHandler("REPLACE_ME", "REPLACE_ME")
    auth.set_access_token('REPLACE_ME','REPLACE_ME')
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
                return pubURL, '[' + authorName + ']' + ' just published a new paper: "' + pubTitle + '"\n' + pubURL + '\n' + authorHandles_dic[authorName]
            else:
                return pubURL, '[' + authorName + ']' + ' just published a new paper: "' + pubTitle + '"\n' + pubURL
    return None
    
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
api = create_api()
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
            newPubIDs.append(pubID)

newPubIDs = list(dict.fromkeys(newPubIDs))
with open('C:/Users/Colton/Github/ScholarBot/pubs.csv','a') as pubFile:
    for pubID in newPubIDs:
        pubFile.write(pubID+'\n')
