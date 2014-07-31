
# coding: utf-8

# In[1]:

import pandas as pd
values_df = pd.read_csv("data/genomic-alterations.tsv", sep="\t", na_values="-")
values_df.head()


# In[16]:

from widget_jheatmap import JHeatmap
JHeatmap(values_df,rows=["samples"],cols=["symbol"], autodraw=False)




