import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# 1. Get your ID Card
credential = DefaultAzureCredential()

# 2. Get your Subscription ID (We will set this as a variable)
sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")

# 3. Initialize the "Remote Control" for Resources
resource_client = ResourceManagementClient(credential, sub_id)

print(f"--- STARTING AZURE AUDIT FOR SUB: {sub_id} ---")

# 4. Ask Azure for a list of all Resource Groups
# In layman terms: "Hey Azure, show me all the folders you have!"
try:
    groups = resource_client.resource_groups.list()
    
    for group in groups:
        print(f"📂 Found Resource Group: {group.name} in {group.location}")

except Exception as e:
    print(f"🚨 Error: Could not talk to Azure. Did you run 'az login'?")
    print(e)

print("--- AUDIT COMPLETE ---")
