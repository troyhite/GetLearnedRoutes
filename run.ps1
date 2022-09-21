# Input bindings are passed in via param block.
param($Timer)
#Subscription
$subscriptionId = '<subid>'
#Resource Group
$resourceGroup = '<resource-group>'
#VPN Gateway associated with vWAN S2S
$vpngw = '<vpn-gateway>'
# Set target Azure Subscription
Set-AzContext -Subscription $subscriptionId
# Set AzRest URI
$restUri = "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.Network/vpnGateways/$vpngw/getlearnedroutes?api-version=2022-01-01"
# Call API and store respone
$response = Invoke-AzRestMethod -Path $restUri -Method POST
# Extract Location Header
$location = $response.Headers.Location.PathAndQuery
# Sleep so API call doesn't return 'null' value
Start-Sleep -Seconds 3
# GET on Location Header Key
$results = Invoke-AzRestMethod -Path $location -Method GET
# Convert Results to JSON
$value = $($results.Content | ConvertFrom-Json ).Value | ConvertTo-Json
# Push JSON to Storage Account
Push-OutputBinding -Name jsonOutput -Value $value