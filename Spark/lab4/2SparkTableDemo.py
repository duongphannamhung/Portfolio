from pyspark import SparkConf
from pyspark.sql import SparkSession

conf = SparkConf().setMaster('local').setAppName('SparkSQLTableDemo')

spark = SparkSession.builder.config(conf=conf).getOrCreate()
sc = spark.sparkContext

DATASET_PATH = 'flight-time.parquet'

flightTimeParquetDF = spark.read.format('parquet').load(DATASET_PATH)

spark.sql('CREATE DATABASE IF NOT EXISTS AIRLINE_DB')
spark.catalog.setCurrentDatabase('AIRLINE_DB')

flightTimeParquetDF.write.mode('overwrite').saveAsTable('flight_data_tbl')

print(spark.catalog.listTables('AIRLINE_DB'))