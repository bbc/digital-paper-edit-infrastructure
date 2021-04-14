from troposphere.s3 import (
    Bucket,
    BucketOwnerFullControl,
    NotificationConfiguration,
    QueueConfigurations,
)
from troposphere.iam import User, InstanceProfile, Policy
from troposphere import Parameter, Ref, Template, Join, GetAtt, Output
from awacs.s3 import PutObject
from awacs.sts import AssumeRole
from awacs.aws import (
    Action,
    Statement,
    Allow,
    Principal,
    Condition,
    PolicyDocument,
)

t = Template()

t.set_description(
    "AWS CloudFormation Sample Template S3_Bucket: Sample template showing "
    "how to create a publicly accessible S3 bucket. "
    "**WARNING** This template creates an Amazon S3 Bucket. "
    "You will be billed for the AWS resources used if you create "
    "a stack from this template."
)

t.set_version("2010-09-09")

s3bucketName = t.add_parameter(Parameter("S3BucketName", Type="String"))

userName = t.add_parameter(Parameter("UserName", Type="String"))

environment = t.add_parameter(Parameter("Environment", Type="String"))

ExternalUploadRole = t.add_resource(
    User(
        "UploadUser",
        UserName=Join("-", [Ref(environment), Ref(userName)]),
        Policies=[
            Policy(
                PolicyName="UploadPolicy",
                PolicyDocument=PolicyDocument(
                    Statement=[
                        Statement(
                            Effect=Allow,
                            Action=[PutObject],
                            Resource=[
                                Join("", ["arn:aws:s3:::", Ref(s3bucketName)]),
                                Join(
                                    "",
                                    ["arn:aws:s3:::", Ref(s3bucketName), "/*"],
                                ),
                            ],
                        )
                    ],
                ),
            )
        ],
    )
)


print(t.to_json())