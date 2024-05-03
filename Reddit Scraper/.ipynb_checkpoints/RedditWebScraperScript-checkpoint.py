import json
import praw
import time
import re
import requests
from bs4 import BeautifulSoup

reddit = praw.Reddit(
    client_id="bwjZyqy7Lplf_jPY5ds3SA",
    client_secret="oMFXunnTXVkqlIMdihJwLVB0HaALsg",
    user_agent="IllSleep4413",
)

seenPosts = []
subredditsToCrawl = ["nba", "warriors", "lakers", "bostonceltics", "torontoraptors", "sixers", "chicagobulls", "rockets", 
                     "NYKnicks", "clevelandcavs", "Thunder", "MkeBucks", "mavericks", "NBASpurs", "timberwolves",
                     "washingtonwizards", "UtahJazz", "ripcity", "suns", "kings", "heat", "denvernuggets", "AtlantaHawks", 
                     "GoNets", "OrlandoMagic", "DetroitPistons", "LAClippers", "pacers", "CharlotteHornets", "NOLAPelicans",
                     "memphisgrizzlies", "NBA_Draft", "VintageNBA", "Nbamemes", "nbadiscussion", "NBA_Bets", "NBA2K", 
                     "NBATalk", "nbabetting", "NBAlive", "nbastreambot", "dfsports", "nbaNews", "Basketball", 
                     "NBA_Highlights", "WholesomeNBA", "sports", "nbacirclejerk", "basketballcards", "CollegeBasketball", 
                     "LukaDoncic", "KobeReps", "lebron"]
currentSubReddit = 0
filesize = 0

while(currentSubReddit < len(subredditsToCrawl) or filesize <= 500000000):
    
    print(subredditsToCrawl[currentSubReddit], len(seenPosts))
    
    for submission in reddit.subreddit(subredditsToCrawl[currentSubReddit]).top(limit=None):
        
        if(submission.id not in seenPosts):
            #print(submission.selftext)
            #print(submission.title)
            #print(submission.id) 
            #print(submission.score) 
            #print(submission.url)
            #print(submission.permalink)
    
            JSONdict = {
                "selftext": submission.selftext,
                "title": submission.title,
                "id": submission.id,
                "created_utc": submission.created_utc,
                "score": submission.score,
                "num_comments": submission.num_comments,
                "upvote_ratio": submission.upvote_ratio,
                "url": submission.url,
                "permalink": submission.permalink
            }
    
            seenPosts.append(submission.id)
            output_file = open("myredditdata.json", "a")
            postString = json.dumps(JSONdict)
            output_file.write(postString + '\n')
            filesize = output_file.tell()

            print(filesize)
            
        if(filesize >= 500000000):
            break
            
    currentSubReddit+=1