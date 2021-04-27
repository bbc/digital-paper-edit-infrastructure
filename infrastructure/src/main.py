import sys

from cosmosTroposphere import CosmosTemplate
from cosmosTroposphere.component.iam import IAM
from troposphere import Join, Output, Parameter, Ref

from troposphere.kms import Alias, Key
from awacs.aws import Policy, Statement, Condition

from awacs.aws import Action, Allow, Principal, Statement, Bool


t = CosmosTemplate(
    description="Digital Paper Edit Infrastructure",
    component_name="digital-paper-edit",
    project_name="news-labs",
)


component_name = t.add_parameter(
    Parameter("ComponentName", Type="String", Description="Your component name")
)


t.resources[IAM.COMPONENT_POLICY].PolicyDocument.Statement.extend(
    [
        Statement(
            Action=[
                Action("kms", "Create*"),
                Action("kms", "Describe*"),
                Action("kms", "Enable*"),
                Action("kms", "List*"),
                Action("kms", "Put*"),
                Action("kms", "Update*"),
                Action("kms", "Revoke*"),
                Action("kms", "Disable*"),
                Action("kms", "Get*"),
                Action("kms", "Delete*"),
                Action("kms", "TagResource*"),
                Action("kms", "UntagResource*"),
                Action("kms", "ScheduleKeyDeletion*"),
                Action("kms", "CancelKeyDeletion*"),
            ],
            Resource=[
                "arn:aws:kms:*:060170161162:key/*",
                "arn:aws:kms:*:060170161162:alias/*",
            ],
            Effect=Allow,
        )
    ]
)

key_policy = Policy(
    Version="2012-10-17",
    Statement=[
        Statement(
            Sid="Enable IAM User Permissions",
            Effect=Allow,
            Principal=Principal("AWS", "arn:aws:iam::060170161162:root"),
            Action=[Action("kms", "*")],
            Resource=["*"],
        ),
        Statement(
            Sid="Allow access for Key Administrators",
            Effect=Allow,
            Principal=Principal(
                "AWS",
                [
                    "arn:aws:iam::060170161162:role/tamsin.green@bbc.co.uk",
                    "arn:aws:iam::060170161162:role/lei.he01@bbc.co.uk",
                ],
            ),
            Action=[
                Action("kms", "Create*"),
                Action("kms", "Describe*"),
                Action("kms", "Enable*"),
                Action("kms", "List*"),
                Action("kms", "Put*"),
                Action("kms", "Update*"),
                Action("kms", "Revoke*"),
                Action("kms", "Disable*"),
                Action("kms", "Get*"),
                Action("kms", "Delete*"),
                Action("kms", "TagResource*"),
                Action("kms", "UntagResource*"),
                Action("kms", "ScheduleKeyDeletion*"),
                Action("kms", "CancelKeyDeletion*"),
            ],
            Resource=["*"],
        ),
        Statement(
            Sid="Allow use of the key",
            Effect=Allow,
            Principal=Principal(
                "AWS",
                [
                    "arn:aws:iam::060170161162:role/anna.blaziak@bbc.co.uk",
                    "arn:aws:iam::060170161162:role/allison.shultes@bbc.co.uk",
                    "arn:aws:iam::060170161162:role/sarah.rainbow@bbc.co.uk",
                ],
            ),
            Action=[
                Action("kms", "Encrypt*"),
                Action("kms", "Decrypt*"),
                Action("kms", "ReEncrypt*"),
                Action("kms", "GenerateDataKey*"),
                Action("kms", "DescribeKey"),
            ],
            Resource=["*"],
        ),
        Statement(
            Sid="Allow attachment of persistent resources",
            Effect=Allow,
            Principal=Principal(
                "AWS",
                [
                    "arn:aws:iam::060170161162:role/anna.blaziak@bbc.co.uk",
                    "arn:aws:iam::060170161162:role/allison.shultes@bbc.co.uk",
                    "arn:aws:iam::060170161162:role/sarah.rainbow@bbc.co.uk",
                ],
            ),
            Action=[
                Action("kms", "CreateGrant"),
                Action("kms", "ListGrants"),
                Action("kms", "RevokeGrant"),
            ],
            Resource=["*"],
            Condition=Condition(Bool({"kms:GrantIsForAWSResource": True})),
        ),
    ],
)

kms_key = t.add_resource(
    Key(
        "KmsKey",
        Description="Key for encrypting the secrets",
        KeyPolicy=key_policy,
    )
)

t.add_output(
    Output(
        "KeyId",
        Value=Ref(kms_key),
        Description="KeyId of KMS",
    )
)


kms_alias = t.add_resource(
    Alias(
        "KeyAlias",
        AliasName=Join(
            "",
            [
                "alias/",
                Ref(component_name),
            ],
        ),
        TargetKeyId=Ref(kms_key),
        DependsOn=kms_key,
    )
)


template = t.to_json()
if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(template + "\n")
else:
    print(template)
