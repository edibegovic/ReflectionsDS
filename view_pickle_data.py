import pandas as pd
#import datetime

df = pd.read_pickle("reddit_experiment_with_comments.pickle")
df[1750:1800]
# date = "2021-04-03"
# date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
# date_time_obj += datetime.timedelta(days=7)
# date_time_obj
# df = df[df["start_date"] != date_time_obj]
# df

# min(df["start_date"])
# for name, group in df.groupby("start_date"):
#     print(name)
#     print(len(group["start_date"]))

# df.to_pickle("reddit_experiment.pickle")