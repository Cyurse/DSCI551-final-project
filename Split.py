from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import split, explode
sc = SparkContext('local')
spark = SparkSession(sc)
df = spark.read.csv('/Users/zhangshengwang/Desktop/DSCI551/Project/video.csv', header=True)

# Split 'Tags' column to create multiple rows for each video_id
df = df.withColumn('tags',explode(split('tags','"')))
df = df.filter((df.tags != '') & (df.tags != '|'))

# Export CSV file
df.repartition(1).write.format("com.databricks.spark.csv").option("header", "true").save("video(split).csv")
