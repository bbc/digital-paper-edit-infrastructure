from troposphere import Parameter, Ref, Template, Join

from troposphere.rds import DBInstance, DBParameterGroup
from troposphere.ec2 import SecurityGroup, SecurityGroupRule

BBC_CIDR_BLOCK = '132.185.0.0/16'

t = Template()

componentName = t.add_parameter(Parameter(
    "ComponentName",
    Type="String",
    Description=("component name")
))

environment = t.add_parameter(Parameter(
    "Environment",
    Type="String",
    Description=("Environment name to check against int, test, or live")
))

dbpassword = t.add_parameter(Parameter(
    "DBPassword",
    NoEcho=True,
    Description="The database admin account password",
    Type="String",
    MinLength="1",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription="must contain only alphanumeric characters."
))

rds_vpc_id = t.add_parameter(Parameter(
    "RdsVpcId",
    Type="String",
    Description="The id of the VPC in which to put the RDS instance"
))

rds_subnet_group_name = t.add_parameter(Parameter(
    "RdsSubnetGroupName",
    Type="String",
    Description="The id of the subnet in which to put the RDS instance"
))

rds_security_group = t.add_resource(SecurityGroup(
    'RdsSecurityGroup',
    VpcId=Ref(rds_vpc_id),
    SecurityGroupIngress=[
        SecurityGroupRule(
            IpProtocol='tcp',
            CidrIp=BBC_CIDR_BLOCK,
            FromPort=5432,
            ToPort=5432
        )
    ],
    GroupDescription='Permit Postgres client access from BBC CIDR block'
))

database = t.add_resource(DBInstance(
    # Join("-",[Ref(environment), Ref(componentName), 'db']),
    "dpeDB",
    AllocatedStorage="10",
    AvailabilityZone='eu-west-1a',
    DBInstanceClass='db.t2.micro',
    # DBName=db_name,
    Engine="postgres",
    EngineVersion="11.4",
    MasterUsername='root',
    MasterUserPassword=Ref(dbpassword),
    PubliclyAccessible=False,
    StorageType='standard',
    DBSubnetGroupName=Ref(rds_subnet_group_name),
    VPCSecurityGroups=[Ref(rds_security_group)],
    DependsOn=['RdsSecurityGroup']
))

print(t.to_json())
