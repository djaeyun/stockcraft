import praw
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',
                     client_id='t28ADFT5o91xmA', client_secret="3ZPcOSR6laQys7nLGoyiy54fU5g",
                     username='stockcraft', password='stockcraft')

submission = reddit.submission(id='acqfgx')

submission.comments.replace_more(limit=0)
for top_level_comment in submission.comments:
        print(top_level_comment.body)

submission.comments.replace_more(limit=0)
for comment in submission.comments.list():
    print(comment.body)