from cosmosTroposphere import CosmosTemplate	
t = CosmosTemplate(description="Digital Paper Edit Infrastructure",	
                   component_name="digital-paper-edit-infrastructure",	
                   project_name="news-labs",	
                   )	
print(t.to_json())