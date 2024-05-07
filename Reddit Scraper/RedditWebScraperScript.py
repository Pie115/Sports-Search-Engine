import praw
import json
import logging
import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
session.mount('https://', HTTPAdapter(max_retries=retries))

reddit = praw.Reddit(client_id="bwjZyqy7Lplf_jPY5ds3SA",
                     client_secret="oMFXunnTXVkqlIMdihJwLVB0HaALsg",
                     user_agent="IllSleep4413")

seenPosts = []
subredditsToCrawl = [] 

embeddedLinks = r'https?:\/\/(?:www\.)?[^\s]+'


def scrapePostLoop(submission, file_name):
    if submission.id not in seenPosts:
        otherUrls = re.findall(embeddedLinks, submission.selftext) + [submission.url]
        print(otherUrls)

        otherUrlList = []
        for i in otherUrls:
            title = "Not Found"
            body = "Not Found"
            url = i.strip()

        try:
            page = session.get(url, timeout=2)
            if not url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    parsed_url = urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    rp = urllib.robotparser.RobotFileParser()
                    rp.set_url(f"{base_url}/robots.txt")
                    rp.read()
                    can_fetch = rp.can_fetch('*', url)
            
                    if can_fetch:
                        page = session.get(url, timeout=3)
                        page.raise_for_status()
                        soup = BeautifulSoup(page.content, "html.parser")
                        title = soup.title.string.strip() if soup.title else title
                        body = soup.get_text(strip=True)
                        print("Title:", title, "Body:", body)
            
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error processing {url}: {e}")
                
            otherUrlDict = {"title": title, "body": body, "url": url}
            otherUrlList.append(otherUrlDict)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error processing {url}: {e}")

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
        with open(file_name, "a") as output_file:
            json.dump(JSONdict, output_file)
            output_file.write('\n')
            output_file.flush()    

def checkForDuplicatesInFile(file_name):
    temp = open(file_name, 'a')
    temp.close()
    
    with open(file_name, 'r') as file:
        for line in file:
            data = json.loads(line)
            if 'id' in data:
                seenPosts.append(data['id'])

def mainCrawlerCode(file_name, subredditsToCrawl, maxFileSize):
    currentSubReddit = 0
    filesize = 0
    while(currentSubReddit < len(subredditsToCrawl) or filesize <= maxFileSize):
        
        print(subredditsToCrawl[currentSubReddit], len(seenPosts))
        
        for submission in reddit.subreddit(subredditsToCrawl[currentSubReddit]).new(limit=None):
            scrapePostLoop(submission, file_name)
            if(filesize >= maxFileSize):
                break
            filesize = os.path.getsize(file_name)
            print(os.path.getsize(file_name))
        for submission in reddit.subreddit(subredditsToCrawl[currentSubReddit]).top(limit=None):
            scrapePostLoop(submission, file_name)
            if(filesize >= maxFileSize):
                break
            filesize = os.path.getsize(file_name)

        for submission in reddit.subreddit(subredditsToCrawl[currentSubReddit]).hot(limit=None):
            scrapePostLoop(submission, file_name)
            if(filesize >= maxFileSize):
                break
            filesize = os.path.getsize(file_name)

        currentSubReddit+=1
        filesize = os.path.getsize(file_name)

def mainUI():
    print("Enter a file you would like to use, make sure the file name ends in .json: ")
    file_name = input()
    print("Enter a subreddit you would like to crawl, if you input multiple subreddits, make sure they are seperated by a singular space: ")
    subredditsString = input()

    temp = ""
    for i in range(len(str(subredditsString))):
        if (subredditsString[i] == " "):
            subredditsToCrawl.append(temp)
            temp = ""
        elif(i == len(subredditsString) - 1):
            temp += subredditsString[i]
            subredditsToCrawl.append(temp)
            temp = ""
        else:
            temp += subredditsString[i]
    print(subredditsToCrawl)
    
    
    print("Enter the amount of space (IN BYTES) that you would like the crawler to stop at: ")
    filesize = input()

    checkForDuplicatesInFile(file_name)
    mainCrawlerCode(file_name, subredditsToCrawl, int(filesize))

mainUI()
