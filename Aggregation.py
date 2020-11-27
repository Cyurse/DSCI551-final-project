import requests
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
import csv

# Aggregate two dataset
# Using video that is not splitted
sc = SparkContext('local')
spark = SparkSession(sc)
video_no_split_before = spark.read.csv('/Users/zhangshengwang/Desktop/DSCI551/Project/video(no_split).csv', header=True)
channel_before = spark.read.csv('/Users/zhangshengwang/Desktop/DSCI551/Project/channels.csv', header = True)

# Keep certain relevant columns
video_no_split = video_no_split_before.select([c for c in video_no_split_before.columns if c in ['video_id',
'title','channel_title','category_id','tags','views','likes','dislikes','comment_count','thumbnail_link','description']])
channel = channel_before.select([c for c in channel_before.columns if c in ['category_id',
'category_name','description','followers','title','videos']])

# Change string to integer
video_no_split.selectExpr("cast(views as int) views","cast(likes as int) likes","cast(dislikes as int) dislikes",
"cast(comment_count as int) comment_count")
channel.selectExpr("cast(followers as int) followers","cast(videos as int) videos")

channel = channel.dropDuplicates(['title'])

# Aggregate two dataset
data_agg = video_no_split.join(channel, video_no_split.category_id == channel.category_id,how='left')

# Create new alias
newNames = ['video_id','video_title', 'channel_title', 'category_ids','tags','views','likes','dislikes',
'comment_count','thumbnail_link','descriptions','category_id','category_name','description','followers','title','videos']
data_agg= data_agg.toDF(*newNames)

# Export to csv
data_agg = data_agg.filter(data_agg.description. isNotNull())
data_agg = data_agg.dropDuplicates(['video_id'])
data_agg.registerTempTable('table')
data_agg = spark.sql("SELECT * FROM (SELECT *, MAX(views) OVER (PARTITION BY video_title) AS maxV FROM table) M WHERE views = maxV")
data_agg.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("data_agg.csv")
