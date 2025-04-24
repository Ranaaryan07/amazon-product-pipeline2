import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType

def transform_data():

    # Create a Spark session
    spark = SparkSession.builder \
        .appName("TransformProductData") \
        .getOrCreate()

    # Define schema for the products data based on our create_products function
    schema = StructType([
        StructField("product_id", StringType(), True),
        StructField("title", StringType(), True),
        StructField("category", StringType(), True),
        StructField("price", FloatType(), True),
        StructField("rating", FloatType(), True),
        StructField("review_count", IntegerType(), True),
        StructField("availability", StringType(), True),
        StructField("timestamp", StringType(), True)
    ])

    # Read data from output folder which is in json format
    df = spark.read.schema(schema).json("/opt/airflow/output")

    # Cleaning the data 
    df_cleaned = df.dropna().dropDuplicates(["product_id"])
    df_transformed = df_cleaned.withColumn("discount_price", col("price") * 0.9)
    df_transformed = df_transformed.withColumn("timestamp", col("timestamp").cast(TimestampType()))

    # Writing the data 
    df_transformed.write.mode("overwrite").parquet("/opt/airflow/transformed/transformed_data.parquet")
    
    # Stop the Spark session
    spark.stop()
