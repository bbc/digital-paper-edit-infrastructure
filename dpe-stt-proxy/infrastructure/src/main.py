from cosmosTroposphere import CosmosTemplate
from cosmosTroposphere.component.iam import IAM
from awacs.aws import Action, Allow, Statement

t = CosmosTemplate(description="Digital Paper Edit STT",
                   component_name="digital-paper-edit-stt",
                   project_name="news-labs",
                   )


t.resources[IAM.COMPONENT_POLICY].PolicyDocument.Statement.extend([
    Statement(
        Action=[
            Action('logs', 'CreateLogGroup'),
            Action('logs', 'CreateLogStream'),
            Action('logs', 'PutLogEvents'),
            Action('logs', 'DescribeLogStreams'),
            Action('sqs', 'ReceiveMessage'),
            Action('sqs', 'DeleteMessage'),
            Action('s3', 'GetObject'),
            Action('s3', 'ListObject'),
        ],
        Resource=[
            "arn:aws:logs:*:*:*",
            "arn:aws:sqs:*:*:*",
            "arn:aws:s3:*:*:*"
        ],
        Effect=Allow
    ),
])


t.resources[IAM.COMPONENT_POLICY].PolicyDocument.Statement.extend([
    Statement(
        Action=[
            Action('logs', 'CreateLogGroup'),
            Action('logs', 'CreateLogStream'),
            Action('logs', 'PutLogEvents'),
            Action('logs', 'DescribeLogStreams'),
            Action('sqs', 'ReceiveMessage'),
            Action('sqs', 'DeleteMessage')
        ],
        Resource=[
            "arn:aws:logs:*:*:*",
            "arn:aws:sqs:*:*:*"
        ],
        Effect=Allow
    ),
])

print(t.to_json())
