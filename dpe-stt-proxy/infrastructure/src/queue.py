import sys
from troposphere import GetAtt, Ref, Template, Join, Parameter
from troposphere.sqs import Queue, QueuePolicy

t = Template()

t.set_description("AWS CloudFormation Sample Template: This template "
                  "demonstrates the creation of a DynamoDB table.")

component = t.add_parameter(Parameter(
    "ComponentName",
    Type="String",
    Description=("Component name")
))

sttGatewayIspyTopic = t.add_parameter(Parameter(
    "SttGatewayIspyTopic",
    Type="String",
    Description=("SttGatewayIspyTopic")
))

sttBridgeAwsIspyTopic = t.add_parameter(Parameter(
    "SttBridgeAwsIspyTopic",
    Type="String",
    Description=("SttBridgeAwsIspyTopic")
))

sttIspyConformerIspyTopic = t.add_parameter(Parameter(
    "SttIspyConformerIspyTopic",
    Type="String",
    Description=("SttIspyConformerIspyTopic")
))

sttNormaliserAwsIspyTopic = t.add_parameter(Parameter(
    "SttNormaliserAwsIspyTopic",
    Type="String",
    Description=("SttNormaliserAwsIspyTopic")
))

sttOutputNotification = t.add_parameter(Parameter(
    "SttOutputNotification",
    Type="String",
    Description=("SttOutputNotification")
))

environment = t.add_parameter(Parameter(
    "Environment",
    Default=".",
    AllowedPattern="^(int|test|live)$",
    Type="String",
    Description=("Environment name to check against int, test, or live")
))

recvWaitSeconds = t.add_parameter(Parameter(
    "ReceiveMessageWaitTimeSeconds",
    Default=20,
    Type="Integer"
))

visTimeout = t.add_parameter(Parameter(
    "VisibilityTimeout",
    Default=30,
    Type="Integer"
))

sqsQueue = t.add_resource(Queue(
    "SQSQueue",
    QueueName=Join("-", [Ref(environment), Ref(component), 'queue']),
    ReceiveMessageWaitTimeSeconds=Ref(recvWaitSeconds),
    VisibilityTimeout=Ref(visTimeout)
))

t.add_resource(QueuePolicy(
    "AllowSNS2SQSPolicy",
    Queues=[Ref(sqsQueue)],
    PolicyDocument={
        "Version": "2008-10-17",
        "Id": "PublicationPolicy",
        "Statement": [{
            "Sid": "PSTT-statement",
            "Effect": "Allow",
            "Principal": {
              "AWS": "*"
            },
            "Action": [
                'sqs:GetQueueUrl',
                'sqs:SendMessage',
                'sqs:GetQueueAttributes'
                ],
            "Resource": GetAtt(sqsQueue, "Arn"),
            'Condition': {
                'ForAnyValue:ArnEquals': {
                    'aws:SourceArn': [
                        Ref(sttBridgeAwsIspyTopic),
                        Ref(sttGatewayIspyTopic),
                        Ref(sttIspyConformerIspyTopic),
                        Ref(sttNormaliserAwsIspyTopic),
                        Ref(sttOutputNotification)
                    ]
                }
            }
        }]
    }
))

template = t.to_json()
if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(template + "\n")
else:
    print(template)
