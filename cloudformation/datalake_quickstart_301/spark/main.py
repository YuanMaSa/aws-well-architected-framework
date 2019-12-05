"""
spark job sample
"""
from __future__ import print_function
import sys
import json
import time
import logging
import textwrap
import boto3
# import datetime
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
# from pyspark.sql.types import *
# from pyspark.sql.functions import *

msg_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
logging.basicConfig(format=msg_format, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("emr_spark_logger")
logger.setLevel(logging.INFO)
spark = SparkSession.builder.appName("SparkIngestionJob").getOrCreate()
sc = SparkContext.getOrCreate()

s3 = boto3.client('s3')
input_obj = s3.get_object(Bucket=sys.argv[1], Key=f'spark/conf/ingestion_path.json')
input_path = list(map(lambda x: x["path"], json.loads(input_obj['Body'].read().decode('utf-8'))))

def main():
    """
    main func
    """
    # load the data from input path
    for path in input_path:
        data = spark.read.format('csv').options(header='true', inferSchema='true').load(path)
        color_type = path.split("/")[-2]

        if color_type == "Green":
            data = data.withColumnRenamed("Trip_type ", "Trip_type")
        # create temp table and generate new dataframe using spark sql
        data.createOrReplaceTempView(color_type.lower())
        df_output = spark.sql(get_sqlsmt(color_type.lower()))

        logger.info(f"create dataframe for {color_type.lower()} taxi data")
        # output the dataframe to s3 with partitioning
        df_output.write.mode("overwrite").partitionBy("year", "month", "day", "hour").save(f"s3://{sys.argv[2]}/{color_type}/")
        logger.info(f"write out dataframe for {color_type.lower()} taxi data")

def get_sqlsmt(color):
    """
    get the sql query from s3
    """
    sql_smt = s3.get_object(Bucket=sys.argv[1], Key=f'spark/sql/{color}.sql')
    sql_smt = textwrap.dedent("""{}""".format(sql_smt['Body'].read().decode('utf-8')))
    return sql_smt

if __name__ == "__main__":
    # sc.install_pypi_package("boto3")
    total_start_time = time.time()
    logger.info("list out the arguments")
    # print arguments
    logger.info(sys.version)
    logger.info(sys.argv[1])
    logger.info(sys.argv[2])

    logger.info("start to run main function")
    # run main function
    main()

    logger.info(
        "total running time of function : --- %s seconds ---"
        %(time.time() - total_start_time)
    )
