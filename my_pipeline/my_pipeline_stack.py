from aws_cdk import (
    # Duration,
    Stack,
    pipelines 
)
import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

from my_pipeline.pipeline_stage import PipelineStage
from aws_cdk.pipelines import ManualApprovalStep

class MyPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = pipelines.CodePipeline(self, "Pipeline",
                        pipeline_name="MyPipeline",
                        synth=ShellStep("Synth",
                            input=CodePipelineSource.git_hub("EXO-BYTE/pipeline", "main"),
                            commands=["npm install -g aws-cdk",
                                "python -m pip install -r requirements.txt",
                                "cdk synth"]
                        )
                    )
        testing_stage = pipeline.add_stage(PipelineStage(self,"testing",
        env=cdk.Environment(account="429005187143", region="us-east-1")))
        
        testing_stage.add_post(ManualApprovalStep('approval to deploy to prod'))
        
        prod_stage = pipeline.add_stage(PipelineStage(self,"production",
        env=cdk.Environment(account="429005187143", region="us-east-1")))