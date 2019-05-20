import sys

import troposphere as Fn
from troposphere import (
    ec2, iam, Template, Parameter, Ref, elasticloadbalancing
)
from troposphere.autoscaling import (
    LaunchConfiguration,
    AutoScalingGroup
)
from troposphere.route53 import RecordSetType
from troposphere.policies import AutoScalingRollingUpdate, UpdatePolicy


HEALTH_CHECK_TARGET = "HTTP:7080/status"

t = Template()
t.add_version("2010-09-09")
t.set_description("Main stack for the sample NodeJS application")

image_id = t.add_parameter(Parameter(
    "ImageId",
    Description=("The AMI used by this component, defaults to base centos 7"),
    Default="ami-9398d3e0",
    Type="AWS::EC2::Image::Id"
))

min_size = t.add_parameter(Parameter(
    "MinSize",
    Description="Minimum number of instances to spin-up",
    Type="String",
    Default="2"
))

max_size = t.add_parameter(Parameter(
    "MaxSize",
    Description="Maximum number of instances to spin-up",
    Type="String",
    Default="2"
))

environment = t.add_parameter(Parameter(
    "Environment",
    Description="The name of the Cosmos environment: int, test, stage or live",
    AllowedValues=["int", "test", "stage", "live"],
    Type="String"
))

instance_type = t.add_parameter(Parameter(
    "InstanceType",
    Description="EC2 instance type to be used",
    Type="String",
    Default="t2.nano"
))

vpc_id = t.add_parameter(Parameter(
    "VpcId",
    Description="The Id of the VPC to attach the environment to",
    Type="AWS::EC2::VPC::Id"
))

key_pair_name = t.add_parameter(Parameter(
    "KeyName",
    Description=("Name of existing EC2 key-pair to enable "
                 "SSH access to the created instances"),
    Type="AWS::EC2::KeyPair::KeyName"
))

bastion_access_sg = t.add_parameter(Parameter(
    "BastionAccessSecurityGroup",
    Description="The security group allowing access from the bastions",
    Type="AWS::EC2::SecurityGroup::Id"
))

update_max_batch_size = t.add_parameter(Parameter(
    "UpdateMaxBatchSize",
    Description=("The maximum number of instances to be killed "
                 "at one time during an ASG update"),
    Default="1",
    Type="String"
))

update_min_in_service = t.add_parameter(Parameter(
    "UpdateMinInService",
    Description=("The minimum number of instances to be killed "
                 "at one time during an ASG update"),
    Default="0",
    Type="String"
))

update_pause_time = t.add_parameter(Parameter(
    "UpdatePauseTime",
    Description=("The time to wait between new instances coming "
                 "online and the next batch being killed during "
                 "an ASG update."),
    Default="PT0S",
    Type="String"
))

private_subnets = t.add_parameter(Parameter(
    "PrivateSubnets",
    Type="List<AWS::EC2::Subnet::Id>",
    Description="Comma separated list of subnets to position the ASG in",
))

public_subnets = t.add_parameter(Parameter(
    "PublicSubnets",
    Type="List<AWS::EC2::Subnet::Id>",
    Description="Comma separated list of subnets to position the ELBs in",
))

cname_entry = t.add_parameter(Parameter(
    "CnameEntry",
    Type="String",
    Description="The cname entry for the component"
))

domain_base = t.add_parameter(Parameter(
    "DomainNameBase",
    Type="String",
    Description=(
        "Base domain name (ending with a '.') "
        "under which new DNS entries are added"
    ),
))

role = t.add_resource(iam.Role(
    "ComponentRole",
    Path="/",
    AssumeRolePolicyDocument={
        "Statement": [{
            "Effect": "Allow",
            "Action": ["sts:AssumeRole"],
            "Principal": {"Service": ["ec2.amazonaws.com"]}
        }],
    }
))

instance_profile = t.add_resource(iam.InstanceProfile(
    "ComponentInstanceProfile",
    Path="/",
    Roles=[Ref(role)]
))

elb_sg = t.add_resource(ec2.SecurityGroup(
    "ELBSecurityGroup",
    VpcId=Ref(vpc_id),
    GroupDescription="Only allow public traffic on 443",
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="443",
            ToPort="443",
            CidrIp="0.0.0.0/0",
        )
    ],
    SecurityGroupEgress=[]
))

elb = t.add_resource(elasticloadbalancing.LoadBalancer(
    'ElasticLoadBalancer',
    Subnets=Ref(public_subnets),
    ConnectionDrainingPolicy=elasticloadbalancing.ConnectionDrainingPolicy(
        Enabled=True,
        Timeout=300,
    ),
    CrossZone=True,
    SecurityGroups=[Ref(elb_sg)],
    Listeners=[
        elasticloadbalancing.Listener(
            LoadBalancerPort="443",
            InstancePort="7443",
            Protocol="tcp",
            InstanceProtocol="tcp"
        ),
    ],
    HealthCheck=elasticloadbalancing.HealthCheck(
        Target=HEALTH_CHECK_TARGET,
        HealthyThreshold="3",
        UnhealthyThreshold="3",
        Interval="15",
        Timeout="10",
    )
))

component_dns = t.add_resource(RecordSetType(
    "ComponentDNS",
    HostedZoneName=Ref(domain_base),
    Comment="CNAME redirect the component ELB",
    Name=Fn.Join(".", [
        Ref(cname_entry),
        Ref(environment),
        Ref(domain_base)
    ]),
    Type="CNAME",
    TTL="60",
    ResourceRecords=[Fn.GetAtt(elb, "DNSName")]
))

asg_security_group = t.add_resource(ec2.SecurityGroup(
    "ASGSecurityGroup",
    VpcId=Ref(vpc_id),
    GroupDescription="Security group for the ASG",
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="7080",
            ToPort="7080",
            SourceSecurityGroupId=Ref(elb_sg)
        ),
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="7443",
            ToPort="7443",
            SourceSecurityGroupId=Ref(elb_sg)
        )
    ],
    SecurityGroupEgress=[]
))

launch_conf = t.add_resource(LaunchConfiguration(
    "ComponentLaunchConfiguration",
    KeyName=Ref(key_pair_name),
    IamInstanceProfile=Ref(instance_profile),
    ImageId=Ref(image_id),
    EbsOptimized=False,
    InstanceMonitoring=False,
    SecurityGroups=[
        Ref(bastion_access_sg),
        Ref(asg_security_group)
    ],
    InstanceType=Ref(instance_type)
))

component_asg = t.add_resource(AutoScalingGroup(
    "ComponentAutoScalingGroup",
    UpdatePolicy=UpdatePolicy(
        AutoScalingRollingUpdate=AutoScalingRollingUpdate(
            PauseTime=Ref(update_pause_time),
            MaxBatchSize=Ref(update_max_batch_size),
            MinInstancesInService=Ref(update_min_in_service),
        )
    ),
    MinSize=Ref(min_size),
    MaxSize=Ref(max_size),
    VPCZoneIdentifier=Ref(private_subnets),
    LaunchConfigurationName=Ref(launch_conf),
    LoadBalancerNames=[Ref(elb)]
))

template = t.to_json()

if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(template + "\n")
else:
    print(template)
