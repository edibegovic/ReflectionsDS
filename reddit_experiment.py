import praw
import random
import pandas as pd
import datetime
from time import sleep
from prawcore.exceptions import Forbidden

number_of_posts = 100
file_name = "Data/reddit_experiment_with_comments_test.pickle"


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
    try:
        submission.upvote()
    except:
        return 0


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
    df = pd.read_pickle(file_name)
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
            "day_0_comments",
            "day_1_comments",
            "day_2_comments",
            "day_3_comments",
            "day_4_comments",
            "day_5_comments",
            "day_6_comments",
        ]
    )


today = datetime.date.today()
count_ex = 0
count_con = 0
error_list = []

try:
    loop = (min(df["start_date"]) + datetime.timedelta(days=6)) <= today or len(df["start_date"]) != 1800
except:
    loop = True

def upvote_retry(post_id):
    try:
        upvote = upvote_single_post(post_id)
        return upvote
    except:
        sleep(60)
        return 1

if loop:
    while count_ex != number_of_posts and count_con != number_of_posts:
        # if len(error_list) == 10:
        #     break
        print(f"New post progress {round(((count_ex + count_con)/(number_of_posts * 2))*100, 2)}%", end='\r')
        posts = get_onehundred_new_posts()
        for post_id in posts:
            if post_id not in df["post_id"] and post_id not in df["post_id"]:
                submission = reddit.submission(post_id)
                com = submission.num_comments
                if submission.score == 1 and com == 0:
                    if random.randint(0, 1) and count_ex != number_of_posts:
                        upvote = 1
                        while upvote == 1:
                            upvote = upvote_retry(post_id)
                        if upvote != 0:
                            df.loc[len(df)] = [today, post_id, "experiment", 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            count_ex += 1
                            print(f"New post progress {round(((count_ex + count_con)/(number_of_posts * 2))*100, 2)}%", end='\r')
                        else:
                            error_list.append(0)
                            print("Sleeping... Please wait.", end='\r')
                            sleep(60)
                    elif count_con != number_of_posts:
                        df.loc[len(df)] = [today, post_id, "control", 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        count_con += 1
                        print(f"New post progress {round(((count_ex + count_con)/(number_of_posts * 2))*100, 2)}%", end='\r')

if today <= (max(df["start_date"]) + datetime.timedelta(days=6)):
    for index, row in df.iterrows():
        print(f"Updating progress {round((index/(len(df. index))*100), 2)}%", end='\r')
        if today <= (row["start_date"] + datetime.timedelta(days=6)):
            try:
                submission = reddit.submission(row["post_id"])
            except:
                print("Sleeping... Please wait.", end='\r')
                sleep(10)
                submission = reddit.submission(row["post_id"])
            if (row["start_date"] + datetime.timedelta(days=1)) == today:
                try:
                    df.loc[index, "day_1"] = submission.score
                    df.loc[index, "day_1_comments"] = submission.num_comments
                except:
                    print("Sleeping... Please wait.", end='\r')
                    sleep(10)
                    try:
                        df.loc[index, "day_1"] = submission.score
                        df.loc[index, "day_1_comments"] = submission.num_comments
                    except Forbidden:
                        df.loc[index, "day_1"] =  df.loc[index, "day_0"]
                        df.loc[index, "day_1_comments"] =  df.loc[index, "day_0_comments"]
            elif (row["start_date"] + datetime.timedelta(days=2)) == today:
                try:
                    df.loc[index, "day_2"] = submission.score
                    df.loc[index, "day_2_comments"] = submission.num_comments
                except:
                    print("Sleeping... Please wait.", end='\r')
                    sleep(10)
                    try:
                        df.loc[index, "day_2"] = submission.score
                        df.loc[index, "day_2_comments"] = submission.num_comments
                    except Forbidden:
                        df.loc[index, "day_2"] =  df.loc[index, "day_1"]
                        df.loc[index, "day_2_comments"] =  df.loc[index, "day_1_comments"]
            elif (row["start_date"] + datetime.timedelta(days=3)) == today:
                try:
                    df.loc[index, "day_3"] = submission.score
                    df.loc[index, "day_3_comments"] = submission.num_comments
                except:
                    print("Sleeping... Please wait.", end='\r')
                    sleep(10)
                    try:
                        df.loc[index, "day_3"] = submission.score
                        df.loc[index, "day_3_comments"] = submission.num_comments
                    except Forbidden:
                        df.loc[index, "day_3"] =  df.loc[index, "day_2"]
                        df.loc[index, "day_3_comments"] =  df.loc[index, "day_2_comments"]
            elif (row["start_date"] + datetime.timedelta(days=4)) == today:
                try:
                    df.loc[index, "day_4"] = submission.score
                    df.loc[index, "day_4_comments"] = submission.num_comments
                except:
                    print("Sleeping... Please wait.", end='\r')
                    sleep(10)
                    try:
                        df.loc[index, "day_4"] = submission.score
                        df.loc[index, "day_4_comments"] = submission.num_comments
                    except Forbidden:
                        df.loc[index, "day_4"] =  df.loc[index, "day_3"]
                        df.loc[index, "day_4_comments"] =  df.loc[index, "day_3_comments"]
            elif (row["start_date"] + datetime.timedelta(days=5)) == today:
                try:
                    df.loc[index, "day_5"] = submission.score
                    df.loc[index, "day_5_comments"] = submission.num_comments
                except:
                    print("Sleeping... Please wait.", end='\r')
                    sleep(10)
                    try:
                        df.loc[index, "day_5"] = submission.score
                        df.loc[index, "day_5_comments"] = submission.num_comments
                    except Forbidden:
                        df.loc[index, "day_5"] =  df.loc[index, "day_4"]
                        df.loc[index, "day_5_comments"] =  df.loc[index, "day_4_comments"]
            elif (row["start_date"] + datetime.timedelta(days=6)) == today:
                try:
                    df.loc[index, "day_6"] = submission.score
                    df.loc[index, "day_6_comments"] = submission.num_comments
                except:
                    print("Sleeping... Please wait.", end='\r')
                    sleep(10)
                    try:
                        df.loc[index, "day_6"] = submission.score
                        df.loc[index, "day_6_comments"] = submission.num_comments
                    except Forbidden:
                        df.loc[index, "day_6"] =  df.loc[index, "day_5"]
                        df.loc[index, "day_6_comments"] =  df.loc[index, "day_5_comments"]

df.to_pickle(file_name)