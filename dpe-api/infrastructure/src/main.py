from cosmosTroposphere import CosmosTemplate
from cosmosTroposphere.component.iam import IAM
from troposphere import Parameter, Template, Join, Ref, GetAtt
from troposphere.sns import Topic
from troposphere.s3 import Bucket, LifecycleConfiguration, LifecycleRule
from awacs.aws import Action, Allow, Statement

component_name = "digital-paper-edit-api"

t = CosmosTemplate(description="Digital Paper Edit API",
                   component_name=component_name,
                   project_name="news-labs",
                   )

t.set_version("2010-09-09")

SNSTopic = t.add_resource(Topic(
    "SNSTopic",
    TopicName=Join("-", [
        Ref(t.parameters["Environment"]),
        component_name,
        "sns"
    ])
))

S3Bucket = t.add_resource(Bucket(
    "S3Bucket",
    BucketName=Join("-", [
        Ref(t.parameters["Environment"]),
        component_name,
        "media"
    ]) 
    # LifecycleConfiguration=LifecycleConfiguration(Rules=[
    #     # Add a rule to
    #     LifecycleRule(
    #         # Rule attributes
    #         Id="S3BucketRule",
    #         Prefix="/only-this-sub-dir",
    #         Status="Enabled",
    #         # Applies to current objects 180 days
    #         ExpirationInDays=180
    #     )
    # ])
))

t.resources[IAM.COMPONENT_POLICY].PolicyDocument.Statement.extend([
    Statement(
        Action=[
            Action('sns', 'Publish')
        ],
        Resource=[Ref(SNSTopic)],
        Effect=Allow
    )])

t.resources[IAM.COMPONENT_POLICY].PolicyDocument.Statement.extend([
    Statement(
        Action=[
            Action('s3', 'ListBucket'),
            Action('s3', '*Object')
        ],
        Resource=[GetAtt(Ref(S3Bucket), "Arn")],
        Effect=Allow
    )])

print(t.to_json())
