# test_spark.py
from pyspark import SparkContext
sc = SparkContext("spark://<master-ip>:7077", "TestApp")
rdd = sc.parallelize(range(100))
print("Sum is:", rdd.sum())
