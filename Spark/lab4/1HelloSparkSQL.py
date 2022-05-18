from pyspark import SparkConf
from pyspark.sql import SparkSession

conf = SparkConf().setMaster('local').setAppName('lab4.1')

spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext

DATASET_PATH = 'sample.csv'

surveyDF = spark.read.option('header','true').option('inferSchema','true').csv(DATASET_PATH)

surveyDF.createOrReplaceTempView('survey_tbl')
countDF = spark.sql('SELECT Country, count(1) AS count from survey_tbl where Age<40 group by Country')

countDF.show()