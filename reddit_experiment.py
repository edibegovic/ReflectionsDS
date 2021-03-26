import praw
import random
from pprint import pprint
import pandas as pd
import datetime

number_of_posts = 500


def user_login(client_id, client_secret, username, password, user_agent):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
        user_agent=user_agent,
    )
    return reddit


reddit = user_login(
    "cHSklB8-UfqhKQ",
    "FYwY4PylgJRvncTq2LtBpJBfCRRB0g",
    "RareBodybuilder3469",
    "sycQyb-suzfo0-fyfmag",
    "Mozilla/5.0",
)


def upvote_single_post(user_id):
    submission = reddit.submission(id=user_id)
    submission.upvote()


def get_onehundred_new_posts():
    """Return list of 100 user_id for upvoted posts."""
    one_hundred_new_posts = []
    for post in reddit.subreddit("all").new():
        try:
            one_hundred_new_posts.append(post.id)
            submission = reddit.submission(id=post.id)
        except:
            one_hundred_new_posts.remove(post.id)
    return one_hundred_new_posts


try:
    df = pd.read_pickle("reddit_experiment.pickle")
except FileNotFoundError:
    df = pd.DataFrame(
        columns=[
            "start_date",
            "post_id",
            "group",
            "day_0",
            "day_1",
            "day_2",
            "day_3",
            "day_4",
            "day_5",
            "day_6",
        ]
    )


today = datetime.date.today()
count_ex = 0
count_con = 0

while count_ex != number_of_posts and count_con != number_of_posts:
    posts = get_onehundred_new_posts()
    for post_id in posts:
        if post_id not in df["post_id"] and post_id not in df["post_id"]:
            submission = reddit.submission(post_id)
            if submission.score == 1:
                if random.randint(0, 1) and count_ex != number_of_posts:
                    upvote_single_post(post_id)
                    df.loc[len(df)] = [today, post_id, "experiment", 2, 0, 0, 0, 0, 0, 0]
                    count_ex += 1
                elif count_con != number_of_posts:
                    df.loc[len(df)] = [today, post_id, "control", 1, 0, 0, 0, 0, 0, 0]
                    count_con += 1


for index, row in df.iterrows():
    if today <= (row["start_date"] + datetime.timedelta(days=6)):
        submission = reddit.submission(row["post_id"])
        if (row["start_date"] + datetime.timedelta(days=1)) == today:
            df.loc[index, "day_1"] = submission.score
        elif (row["start_date"] + datetime.timedelta(days=2)) == today:
            df.loc[index, "day_2"] = submission.score
        elif (row["start_date"] + datetime.timedelta(days=3)) == today:
            df.loc[index, "day_3"] = submission.score
        elif (row["start_date"] + datetime.timedelta(days=4)) == today:
            df.loc[index, "day_4"] = submission.score
        elif (row["start_date"] + datetime.timedelta(days=5)) == today:
            df.loc[index, "day_5"] = submission.score
        elif (row["start_date"] + datetime.timedelta(days=6)) == today:
            df.loc[index, "day_6"] = submission.score

df.to_pickle("reddit_experiment.pickle")