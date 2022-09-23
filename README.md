<img src="https://www.appliedis.com/wp-content/uploads/2019/06/Azure-Virtual-WAN-Icon.png" width="50%" height="50%">

# GetLearnedRoutes
Retrieve Learned Routes from a Site-to-Site VPN Gateway associated with Azure Virtual WAN by utilizing the new getlearnedroutes?api-version=2022-01-01 and export the results as a flat JSON file to the storage account for the Azure Function.
# Prerequisities

* Azure Virtual WAN w/ Virtual Hub.
* VPN Site configured on the Virtual Hub.
* Azure Function w/ a timer trigger function created.
* User Created Managed Identity.
## Managed identities in Azure Functions

You can learn more about [managed identities](https://docs.microsoft.com/azure/app-service/overview-managed-identity) and common scenarios in the [documentation](https://docs.microsoft.com/azure/app-service/overview-managed-identity#obtaining-tokens-for-azure-resources).

Another common scenario is to grant the managed identity access to either resource groups or subscriptions so that the function has permissions to take action on Azure resources. This is useful when using functions to automate Azure operational tasks.

This particular example utilizies a User Created Managed Identity. An few extra steps are needed to utilize a user created managed identity. You need to enable the SYSTEM assigned managed identity (along with your user created managed identity) and give the 'Reader' role to the SYSTEM MI on the USER MI. The below command is found in the profile.ps1 file. This method is preferred since it doesn't require hardcoding the 'ClientId' in the Connect-AzAccount command.

```powershell
if ($env:MSI_SECRET) {
    Disable-AzContextAutosave -Scope Process | Out-Null
    Connect-AzAccount -Identity
    $identity = Get-AzUserAssignedIdentity -ResourceGroupName rg -Name mi
    Connect-AzAccount -Identity -AccountId $identity.ClientId
}
```
## Grant the managed identity contributor access to the subscription or resource group so it can perform actions

The below command sets the access at the subscription level.

```powershell
$Context = Get-AzContext
New-AzRoleAssignment -ObjectId <principalId> -RoleDefinitionName Contributor -Scope "/subscriptions/$($Context.Subscription)"
```
For more information about Azure Functions, see the [Azure Functions Overview](https://azure.microsoft.com/documentation/articles/functions-overview/).


