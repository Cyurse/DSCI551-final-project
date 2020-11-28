import pandas as pd 
import numpy as np

df_video = pd.read_csv('USvideos.csv')
df_channel = pd.read_csv('channels.csv')

# Split the 'tags' column with '|' in order to manipulate different keywords in one tag
df_video['tags'][0:100] = df_video['tags'][0:100].str.split("|")
#print(df_video['tags'][0:100])

# Remove missing values in 'tags' column in videos dataset 
# Remove rows which contain missing valus
df_video = df_video.dropna(axis = 0, how = 'any')
df_video = df_video.loc[~df_video['tags'].str.contains('none', na = True) |  (~df_video['tags'].str.contains('NA', na = True))]
print(df_video)

# Remove missing values in 'category_name' column in channels dataset
# Remove rows which conatin missing values
df_channel = df_channel.loc[~df_channel['category_name'].str.contains('none', na = True) |  (~df_channel['category_name'].str.contains('NA', na = True))]
df_channel.dropna(axis = 0, how = 'any')
