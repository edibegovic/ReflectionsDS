
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_pickle("Data/reddit_experiment_with_comments_cut.pickle")

upvotes = df.iloc[:, :10]

control = df[df['group'] == 'control']
experiment = df[df['group'] == 'experiment']

bins=range(10)
plt.hist([control['day_3'], experiment['day_3']], bins, density=True, label=['Control', 'Treatment'])
plt.legend(loc='upper right')
plt.xlabel('Upvotes');
plt.ylabel('Posts')
plt.show()

df.iloc[1855, :]

test = control[control['day_3'] < 100]

len([x for x in (test['day_3']-test['day_6']) if x > 0])

len(test)

print(234569)
print(999990)
o
