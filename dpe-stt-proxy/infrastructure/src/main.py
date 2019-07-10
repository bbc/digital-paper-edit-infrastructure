from cosmosTroposphere import CosmosTemplate
t = CosmosTemplate(description="Digital Paper Edit STT",
                   component_name="digital-paper-edit-stt",
                   project_name="news-labs",
                   )

print(t.to_json())
