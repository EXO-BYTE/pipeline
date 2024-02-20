import aws_cdk as cdk
from constructs import Construct
from aws_cdk_pipeline_demo.glue_demo_stack import GlueDemoStack

class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        glueStack = GlueDemoStack(self, "glueStack")