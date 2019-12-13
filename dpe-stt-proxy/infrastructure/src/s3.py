from troposphere.s3 import Bucket, BucketOwnerFullControl
from troposphere.iam import Role, InstanceProfile, Policy
from troposphere import Parameter, Ref, Template, Join, GetAtt, Output
from awacs.s3 import PutObject
from awacs.sts import AssumeRole
from awacs.aws import Action, Statement, Allow, Principal, Condition, PolicyDocument

t = Template()

t.set_description(
    "AWS CloudFormation Sample Template S3_Bucket: Sample template showing "
    "how to create a publicly accessible S3 bucket. "
    "**WARNING** This template creates an Amazon S3 Bucket. "
    "You will be billed for the AWS resources used if you create "
    "a stack from this template.")

t.set_version("2010-09-09")

s3bucketName = t.add_parameter(Parameter(
    "S3bucket",
    Type="String"
))

roleName = t.add_parameter(Parameter(
    "RoleName",
    Type="String"
))

environment = t.add_parameter(Parameter(
    "Environment",
    Type="String"
))

S3bucket = t.add_resource(Bucket(
    "S3Bucket",
    BucketName=Join("-", [Ref(environment), Ref(s3bucketName)])
))


UploaderRole = t.add_resource(Role(
    "UploaderRole",
    AssumeRolePolicyDocument=PolicyDocument(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[AssumeRole],
                Principal=Principal("AWS", "*"),
            )
        ]
    ),
    RoleName=Join("-", [Ref(environment), Ref(roleName)]),
    Policies=[Policy(
        PolicyName="UploadPolicy",
        PolicyDocument=PolicyDocument(
            Statement=[
                Statement(
                    Effect=Allow,
                    Action=[PutObject],
                    Resource=[GetAtt(S3bucket, "Arn")],
                )
            ])
    )]
))


print(t.to_json())
