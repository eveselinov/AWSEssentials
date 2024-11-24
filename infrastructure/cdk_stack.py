from aws_cdk import (
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_s3_notifications as s3n,
    core
)

class FileProcessingStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, "FileStorageBucket")
        table = dynamodb.Table(
            self, "MetadataTable",
            partition_key={"name": "file_name", "type": dynamodb.AttributeType.STRING}
        )

        lambda1 = _lambda.Function(
            self, "Lambda1ProcessFile",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda1_process_file.lambda_handler",
            code=_lambda.Code.from_asset("lambda")
        )

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(lambda1)
        )

        table.grant_write_data(lambda1)
