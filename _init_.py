import requests
import json
import time
import datetime
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # Set up Azure Key Vault Secrets client
    keyVaultName = 'alz-kv-001'
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    # Get input bindings from Azure Key Vault Secrets
    subscriptionId = client.get_secret('subscription-id').value
    resourceGroup = client.get_secret('resource-group').value
    vpngw = client.get_secret('vpn-gateway').value
    storageAccountName = client.get_secret('storage-account').value
    containerName = client.get_secret('container-name').value
    blobName = client.get_secret('blob-name').value

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
    url = f"https://{storageAccountName}.blob.core.windows.net/{containerName}/{blobName}.json"
    headers = {'Content-Type': 'application/json'}
    requests.put(url, headers=headers, data=json.dumps(value))