from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark import SparkConf


conf = SparkConf().setMaster('local').setAppName('hello')
spark = SparkSession.builder.config(conf=conf) \
      .getOrCreate()
sc = spark.sparkContext


lines = sc.textFile("../data/people.txt")
parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: Row(name=p[0], age=int(p[1])))

# Infer the schema, and register the DataFrame as a table.
schemaPeople = spark.createDataFrame(people)
schemaPeople.show()
schemaPeople.createOrReplaceTempView("people")

# SQL can be run over DataFrames that have been registered as a table.
teenagers = spark.sql("SELECT name as nm FROM people WHERE age >= 13 AND age <= 19")
teenagers.show()

# The results of SQL queries are Dataframe objects.
# rdd returns the content as an :class:`pyspark.RDD` of :class:`Row`.
teenNames = teenagers.rdd.map(lambda p: "Name: " + p.nm).collect()
for name in teenNames:
    print(name)
