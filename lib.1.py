import praw
import pandas as pd
pd.set_option('display.max_columns', 500)
import os
import nltk

reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                     username=os.environ["REDDIT_USERNAME"], password=os.environ["REDDIT_PASSWORD"])

submission = reddit.submission(id='ae67yi')

comment_list = []
for comment in submission.comments.list():
        comment_dict = {}
        comment_dict["author"] = comment.author
        comment_dict["created"] = comment.created
        comment_dict["body"] = comment.body
        # comment_dict["upvote"] = comment.upvote
        # comment_dict["downvote"] = comment.downvote
        comment_list.append(comment_dict) 

df = pd.DataFrame(comment_list)

company_dict = {}
company_dict["google"] = ["google", "goog"]
company_dict["amazon"] = ["amazon","amzn"]
company_dict["apple"] = ["apple","appl"]
company_dict["micron"] = ["micron","mu"]
company_dict["organogenesis holdings"] = ["organogenesis holdings","orgo"]

def recognize_company(row):
        body = row.body
        print("\n\n",body)
        recognized_companies = []
        for key,value in company_dict.items():
                print(key,value)
                for text in value:
                        print(text)
                        if text in body.lower():
                                print("match")
                                recognized_companies.append(key) 
        print(recognized_companies)
        return recognized_companies

df["companies"] = df.apply(lambda row:recognize_company(row),axis=1)