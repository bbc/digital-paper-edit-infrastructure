from troposphere import Parameter, Ref, Template, Join, GetAtt, Output
from troposphere.logs import LogGroup, LogStream
import sys

t = Template()

t.set_version("2010-09-09")

logGroupName = t.add_parameter(Parameter(
    "LogGroupName",
    Type="String"
))

environment = t.add_parameter(Parameter(
    "Environment",
    Type="String"
))

LogGroup = t.add_resource(LogGroup(
    "LogGroup",
    LogGroupName=Join("-", [Ref(environment), Ref(logGroupName)]),
    RetentionInDays=14
))

template = t.to_json()
if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(template + "\n")
else:
    print(template)
