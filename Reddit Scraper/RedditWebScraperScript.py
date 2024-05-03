import json
import praw
import time
import re
import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import logging

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
embeddedLinks = r'https?:\/\/(?:www\.)?[^\s]+'


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

            otherUrlList = []
            otherUrls = re.findall(embeddedLinks, submission.selftext)
            otherUrls.append(submission.url)
            print(otherUrls)

            for i in otherUrls:
                title = "Not Found"
                body = "Not Found"
                url = i
                can_fetch = False
            
                try:
                    url = i.strip()
                    parsed_url = urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    rp = urllib.robotparser.RobotFileParser()
                    rp.set_url(f"{base_url}/robots.txt")
                    rp.read()
                    can_fetch = rp.can_fetch('*', url)
            
                    if can_fetch:
                        page = requests.get(url)  
                        page.raise_for_status()  
                        soup = BeautifulSoup(page.content, "html.parser")
                        if soup.title:
                            title = soup.title.string.strip()
                        if soup.get_text():
                            body = soup.get_text(strip=True)
                        print("Title:", title, "Body:", body)
            
                except Exception as e:
                    logging.error(f"Error processing {url}: {e}")

                otherUrlDict = {
                    "title": title,
                    "body": body,
                    "url": url
                }
                otherUrlList.append(otherUrlDict)
                
            JSONdict = {
                "title": submission.title,
                "self_text": submission.selftext,
                "id": submission.id,
                "created_utc": submission.created_utc,
                "score": submission.score,
                "num_comments": submission.num_comments,
                "upvote_ratio": submission.upvote_ratio,
                "url": submission.url,
                "perma_link": submission.permalink,
                "Embedded_Links": otherUrlList
            }
    
            seenPosts.append(submission.id)
            output_file = open("myredditdata.json", "a")
            postString = json.dumps(JSONdict)
            output_file.write(postString + '\n')
            filesize = output_file.tell()
            
        if(filesize >= 500000000):
            break
            
    currentSubReddit+=1
