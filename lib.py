import praw
import pandas as pd
pd.set_option('display.max_columns', 500)
import os
import bs4 as bs
import pickle
import requests
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                     username=os.environ["REDDIT_USERNAME"], password=os.environ["REDDIT_PASSWORD"])

submission = reddit.submission(id='ah2hwz')

comment_list = []
submission.comments.replace_more(limit=0)
for comment in submission.comments.list():
        comment_dict = {}
        comment_dict["author"] = comment.author
        comment_dict["created"] = comment.created
        comment_dict["body"] = comment.body
        # comment_dict["upvote"] = comment.upvote
        # comment_dict["downvote"] = comment.downvote
        comment_list.append(comment_dict) 

df = pd.DataFrame(comment_list)

#Use Wikipedia's S&P 500 List to grab top 500 Names & Tickers
#Problem: How to remove "Inc." in company names?
resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
soup = bs.BeautifulSoup(resp.text, 'lxml')
table = soup.find('table', {'class':'wikitable sortable'})

company_dict = {}
tickers = []
for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
names = []
for row in table.findAll('tr')[1:]:
        name = row.findAll('td')[1].text
        names.append(name)
for i in range(len(names)):
        company_dict[names[i]] = [names[i], tickers[i]]

def recognize_company(row):
        body = row.body
        #print("\n\n",body)
        recognized_companies = []
        for key,value in company_dict.items():
                #print(key,value)
                for text in value:
                        #print(text)
                        if text in body.lower():
                                #print("match")
                                recognized_companies.append(key) 
        #print(recognized_companies)
        return recognized_companies

df["companies"] = df.apply(lambda row:recognize_company(row),axis=1)

sentim_analyzer = SentimentAnalyzer()
sid = SentimentIntensityAnalyzer()

def sentiment_analysis(row):
        body = row.body
        sentences = tokenize.sent_tokenize(body)
        ratings = []
        for sentence in sentences:
                ss = sid.polarity_scores(sentence)
                ratings.append(ss)
        negatives = 0
        positives = 0
        neutrals = 0
        for r in ratings:
                negatives += r["neg"]
                positives += r["pos"]
                neutrals += r["neu"]
        maxx = max([negatives, positives, neutrals])
        if positives == maxx:
                return "positive"
        if negatives == maxx:
                return "negative"
        if neutrals == maxx:
                return "neutral"
        
df["sentiment"] = df.apply(lambda row:sentiment_analysis(row),axis=1)

#did stock rise or fall within a day of this comment
#function that looks at each row, company, time, then figures out what stock price was 24 hrs later
#then see if it's a rise/fall. stock access api to get
#probably want to get more threads - all threads in past 2 weeks = "what are your moves tomorrow"
#then get all the comments on those threads
#try to generate stock list automatically - same api to get stock prices also get stock names
