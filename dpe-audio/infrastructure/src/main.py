from cosmosTroposphere import CosmosTemplate
from cosmosTroposphere.component.iam import IAM
from troposphere import Parameter, Template, Join, Ref, GetAtt
from awacs.aws import Action, Allow, Statement

component_name = "digital-paper-edit-api"

t = CosmosTemplate(description="Digital Paper Edit API",
                   component_name=component_name,
                   project_name="news-labs",
                   )

t.set_version("2010-09-09")

t.resources[IAM.COMPONENT_POLICY].PolicyDocument.Statement.extend([
    Statement(
        Action=[
            Action('sns', 'Publish')
        ],
        Resource=[Ref(SNSTopic)],
        Effect=Allow
    )])

print(t.to_json())
