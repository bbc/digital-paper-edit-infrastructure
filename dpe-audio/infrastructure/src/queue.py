# originally from https://github.com/cloudtools/troposphere/blob/master/examples/IAM_Policies_SNS_Publish_To_SQS.py

# Converted from IAM_Policies_SNS_Publish_To_SQS.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import GetAtt, Output, Ref, Template, Join
from troposphere.sns import Subscription, Topic
from troposphere.sqs import Queue, QueuePolicy

t = Template()

t.set_description("AWS CloudFormation Sample Template: This template "
                  "demonstrates the creation of a DynamoDB table.")

component = t.add_parameter(Parameter(
    "ComponentName",
    Type="String",
    Description=("Environment name to check against int, test, or live")
))

environment = t.add_parameter(Parameter(
    "Environment",
    Default=".",
    AllowedPattern="^(int|test|live)$",
    Type="String",
    Description=("Environment name to check against int, test, or live")
))

dpeTopic = t.add_parameter(Parameter(
    "dpeTopic",
    Default="",
    Type="String",
    Description=("SNS topic from the DPE API")
))

sqsqueue = t.add_resource(Queue(
    "SQSQueue",
    QueueName=Join("-",[Ref(environment), Ref(component), 'queue'])
))

t.add_resource(QueuePolicy(
    "AllowSNS2SQSPolicy",
    Queues=[Ref(sqsqueue)],
    PolicyDocument={
        "Version": "2008-10-17",
        "Id": "PublicationPolicy",
        "Statement": [{
            "Sid": "audio-converter-statement",
            "Effect": "Allow",
            "Principal": {
              "AWS": "*"
            },
            "Action": [
                'sqs:GetQueueUrl',
                'sqs:SendMessage',
                'sqs:GetQueueAttributes'
                ],
            "Resource": GetAtt(sqsqueue, "Arn"),
            'Condition': {
            'ForAnyValue:ArnEquals': {
            'aws:SourceArn': [
                Ref(dpeTopic)
            ]
          }
        }
        }]
    }
))

print(t.to_json())
