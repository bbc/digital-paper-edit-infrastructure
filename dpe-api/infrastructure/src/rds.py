import sys

from troposphere import Parameter, Ref, Template, Join, GetAtt, Output
from troposphere.ec2 import SecurityGroup, SecurityGroupIngress
from troposphere.rds import DBInstance, DBSubnetGroup

t = Template()

t.add_version("2010-09-09")

allocated_storage = t.add_parameter(Parameter(
    "AllocatedStorage",
    Default="20",
    Type="Number",
    MinValue="5",
    MaxValue="1024",
    ConstraintDescription="must be between 5 and 1024Gb.",
    Description="The amount of storage (in gibibytes) to allocate for the DB "
                "instance."
))

api_security_group_id = t.add_parameter(Parameter(
    "APISecurityGroupID",
    Description="The SecurityGroupID of the API EC2 instance",
    Type="String"
))

subnet_group = t.add_resource(DBSubnetGroup(
    "DBSubnetGroup",
    DBSubnetGroupDescription="Subnets available for the RDS DB Instance",
    SubnetIds=["subnet-1f2a9046", "subnet-19cdad6e", "subnet-19cdad6e"]
))

security_group = t.add_resource(SecurityGroup(
    "SecurityGroup",
    GroupDescription="Enable access to this RDS instance from specific EC2 instances only",
    VpcId="vpc-604fc005",
))

security_group_ingress = t.add_resource(SecurityGroupIngress(
    "PostgresSecurityGroupIngress",
    IpProtocol="tcp",
    FromPort="5432",
    ToPort="5432",
    SourceSecurityGroupId=Ref(api_security_group_id),
    GroupId=Ref(security_group)
))

db_instance_class = t.add_parameter(Parameter(
    "DBClass",
    Default="db.t2.micro",
    Description="The compute and memory capacity of the DB instance, "
                "for example, db.m4.large.",
    Type="String",
    ConstraintDescription="must select a valid database instance type.",
))

component_name = t.add_parameter(Parameter(
    "ComponentName",
    Type="String",
    Description="Your component name"
))

environment = t.add_parameter(Parameter(
    "Environment",
    Type="String",
    Description="Environment name"
))


engine_ver = t.add_parameter(Parameter(
    "DBEngineVersion",
    Description="The version number of the database engine to use.",
    Type="String",
    Default="11.4"
))

dbname = t.add_parameter(Parameter(
    "DBName",
    Default="MyDatabase",
    Description="The database name",
    Type="String",
    MinLength="1",
    MaxLength="64",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("must begin with a letter and contain only"
                           " alphanumeric characters.")
))

dbuser = t.add_parameter(Parameter(
    "DBUser",
    NoEcho=True,
    Description="The database admin account username",
    Type="String",
    MinLength="1",
    MaxLength="63",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("must begin with a letter and contain only"
                           " alphanumeric characters.")
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

db_instance_class = t.add_resource(DBInstance(
    "DBInstance",
    DBName="postgres",
    AllocatedStorage="10",
    DBInstanceClass=Ref(db_instance_class),
    DBInstanceIdentifier=Join(
        "-", [Ref(environment), Ref(component_name),
             "postgres"]
    ),
    Engine="postgres",
    EngineVersion=Ref(engine_ver),
    MasterUsername=Ref(dbuser),
    MasterUserPassword=Ref(dbpassword),
    DBSubnetGroupName=Ref(subnet_group),
    VPCSecurityGroups=[Ref(security_group)],
))


template = t.to_json()

t.add_output(Output(
    "JDBCConnectionString",
    Description="JDBC connection string for database",
    Value=Join("", [
        "jdbc:postgresql://",
        GetAtt("DBInstance", "Endpoint.Address"),
        GetAtt("DBInstance", "Endpoint.Port"),
        "/",
        Ref(dbname)
    ])
))


if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(template + "\n")
else:
    print(template)
