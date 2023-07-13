import requests
import json
import time

# Input bindings are passed in via param block.
# Subscription
subscriptionId = '<subid>'
# Resource Group
resourceGroup = '<resource-group>'
# VPN Gateway associated with vWAN S2S
vpngw = '<vpn-gateway>'
# Set target Azure Subscription
restUri = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Network/vpnGateways/{vpngw}/getlearnedroutes?api-version=2022-01-01"
# Call API and store response
response = requests.post(restUri)
# Extract Location Header
location = response.headers['Location']
# Sleep so API call doesn't return 'null' value
time.sleep(3)
# GET on Location Header Key
results = requests.get(location)
# Convert Results to JSON
value = json.loads(results.content)['value']
# Push JSON to Storage Account
# Replace <storage-account-name> with the name of your storage account
url = f"https://<storage-account-name>.blob.core.windows.net/<container-name>/<blob-name>.json"
headers = {'Content-Type': 'application/json'}
requests.put(url, headers=headers, data=json.dumps(value))