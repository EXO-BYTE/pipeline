from aws_cdk import (
    aws_glue as glue,
    aws_iam as iam,
    aws_s3 as s3,
    Stack,
    aws_s3_deployment as s3_deployment
    # aws_sqs as sqs,
)
from constructs import Construct

class GlueDemo(Stack):
     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_bucket = s3.Bucket(self, "SourceBucket", bucket_name="my-source-bucket-demo-1239")
        destination_bucket = s3.Bucket(self, "DestinationBucket", bucket_name="my-destination-bucket-demo-1239")
        etl_job_script_bucket = s3.Bucket(self, "EtlScriptBucket", bucket_name="my-etl-script-bucket-demo-1239")
        
        s3_deployment.BucketDeployment(
            self,
            "DeployETLScript",
            sources=[s3_deployment.Source.asset("./scripts/")],
            destination_bucket=etl_job_script_bucket,
            destination_key_prefix='etl'
        )

        # Define an IAM role for the Glue job
        glue_job_role = iam.Role(
            self, "GlueJobRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
        )

        # Define an AWS Glue ETL job
        glue_job = glue.CfnJob(
            self, "MyGlueJob",
            role=glue_job_role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location=f"s3://{etl_job_script_bucket.bucket_name}/etl/glue-etl-job.py",  # Specify your Glue ETL script location
            ),
            default_arguments={
                "--sourceBucket": source_bucket.bucket_name,
                "--destinationBucket": destination_bucket.bucket_name,
            },
            glue_version='3.0'
        )