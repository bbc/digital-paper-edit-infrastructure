from cosmosTroposphere import CosmosTemplate
t = CosmosTemplate(description="Digital Paper Edit API",
                   component_name="digital-paper-edit-api",
                   project_name="news-labs",
                   )
print(t.to_json())
