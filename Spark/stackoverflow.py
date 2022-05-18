from pyspark.sql import SparkSession, Window, Row, functions as f
from pyspark.sql.functions import *
from pyspark.sql.types import *

# from pyspark

spark = SparkSession \
    .builder \
    .master('local[3]') \
    .appName('Stack Over Flow Tracking') \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
	.config('spark.jars.packages','org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2') \
	.config('spark.jars.packages','org.mongodb.spark:mongo-spark-connector:10.0.1') \
    .getOrCreate()
    # .config('spark.mongodb.input.uri', 'mongodb://127.0.0.1/dep303-assignment1.') \
    # .config('spark.mongodb.output.uri', 'mongodb://127.0.0.1/dep303-assignment1.') \

# 2. Đọc dữ liệu từ MongoDB với Spark
questions = spark.read \
    .format('com.mongodb.spark.sql.connector.MongoTableProvider') \
    .option("spark.mongodb.connection.uri",'mongodb://127.0.0.1/') \
    .option("spark.mongodb.database",'dep303-assignment1') \
    .option("spark.mongodb.collection",'questions') \
    .load() \

# questions.show()
# questions.printSchema()

# 3. Chuẩn hóa dữ liệu
question_df = questions \
	.withColumn("ClosedDate", to_date(expr("case when ClosedDate == 'NA' then NULL else ClosedDate end"), "yyyy-MM-dd'T'HH:mm:ss'Z'")) \
	.withColumn("CreationDate", to_date(expr("case when CreationDate == 'NA' then NULL else CreationDate end"), "yyyy-MM-dd'T'HH:mm:ss'Z'")) \
	.withColumn("OwnerUserId", expr("case when OwnerUserId == 'NA' then NULL else CAST(OwnerUserId as int) end"))

# question_df.show()
# question_df.printSchema()

# 4. Yêu cầu 1: Tính số lần xuất hiện của các ngôn ngữ lập trình
# Select only cột Body để nhẹ dữ liệu
splitquestion_df = question_df.select("body")

# Split cột ra thành array tập hợp từ
splitquestion_df = splitquestion_df.select(split(splitquestion_df.body, '\s+').alias('split'))

# Chuyển array tập hợp từ sang word từng dòng
splitquestion_df = splitquestion_df.select(explode_outer('split').alias('word'))

# Chỉ chọn các word trong tập hợp
list = ['Java', 'Python', 'C++', 'C#', 'Go', 'Ruby', 'Javascript', 'PHP', 'HTML', 'CSS', 'SQL']
splitquestion_df = splitquestion_df.where(splitquestion_df.word.isin(list))
# splitquestion_df.show()
splitquestion_df = splitquestion_df.groupBy('word').agg(f.count('word').alias('count')).show()
