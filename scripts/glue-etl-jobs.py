import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME","sourceBucket","destinationBucket"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

source_bucket = args['sourceBucket']
destion_bucket = args['destinationBucket']
# Script generated for node Amazon S3
AmazonS3_node1707478163398 = glueContext.create_dynamic_frame.from_options(
    format_options={
        "quoteChar": '"',
        "withHeader": True,
        "separator": ",",
        "optimizePerformance": False,
    },
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": [f"s3://{source_bucket}/glueDemo.csv"],
        "recurse": True,
    },
    transformation_ctx="AmazonS3_node1707478163398",
)

# Script generated for node Amazon S3
AmazonS3_node1707478167284 = glueContext.write_dynamic_frame.from_options(
    frame=AmazonS3_node1707478163398,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": f"s3://{destion_bucket}/output/",
        "partitionKeys": [],
    },
    format_options={"compression": "snappy"},
    transformation_ctx="AmazonS3_node1707478167284",
)

job.commit()