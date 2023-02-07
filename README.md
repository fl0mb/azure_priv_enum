# azure_priv_enum

azure_priv_enum is a tool to gather all the permissions an identity could have in Azure.

This can be difficult due to:

1. The amount of different existing tools, provided by Microsoft:
 - Azure Az powershell 
 - MSOnline powershell 
 - AzureAD powershell  
 - AzureADPreview powershell 
 - Microsoft Graph Powershell
 - Azure CLI
 - SDKs for most well known programming languages
 - Multiple REST APIs, each one available in multiple different versions

2. Insufficient documentation and odd default behavior in those tools:

    The az cli documentation for example, states that the following command lists role assignments:
    ```
    az role assignment list
    ```

    By default however that az command only applies to the currently selected subscription. Additional arguments are needed to also not list roles assigned to groups, inherited roles or classic administrators. This is unintuitive and many role assignments could therefor be missed.

3. The manny different ways some kind of privilege could be applied to an identity:
 - AzureAD Role Assignments 
 - AzureRM Role Assignments 
 - Classic Administrators
 - App Role Assignments/API Permissions 
 - PIM Eligible Role Assignments (AzureAD / AzureRM)
 - Application Ownership --> allows one to act as the application by adding credentials
 - Group owners --> do not count as a member of the group and do therefor not share the same permissions. Are able to add themselves.

| Type  | User | Group  | Service-Principal |
| --- | --- | ---| --- |
| AzureAD Role Assignments | x | x | x |
| AzureRM Role Assignments | x | x | x |
| Classic Administrators | x | - | - |
| App Role Assignments | x | x | x |
| PIM Eligible Role Assignments | x | x | - |
| Application Ownership| x | - | -  |
| Group owners| x | - | x |


4. Different feature sets depending on the AzureAD licensing.

The goal of this tool is to find every privilege a given identity might have, including nested assignments via groups or PIM eligible assignments.

## Usage
In order to run it, a privileged user with global read access is recommended. 
Only a tenant-id/domain and the identity to query are needed to start:

```bash
python az.py -t 94c579f8-ac71-4528-9fde-7c56a007991b -i 83c6f248-97b4-41b7-941d-7c56a007991b

python az.py -d xyz.onmicrosoft.com -i 83c6f248-97b4-41b7-941d-7c56a007991b

python az.py -d xyz.onmicrosoft.com -u user@xyz.onmicrosoft.com
```
If no refresh-token is provided, a device code flow will be started and the resulting tokens are saved to disk (tokens.json).

**Do not forget to delete local files.**

Keep in mind there could still be ACLs and resource level policies.


When leaked credentials are found in an assessment, it could be hard to determine what kind of identity they might belong to.
Therefor, the -i parameter accepts object-ids of users, groups, service principals, app registrations and client-ids.
The initial output will show you the kind of identity provided. 


```
-t / --tenant-id
-d / --domain
-r / --refresh-token
-i / --object-id
-u / --user-principal
-c / --clear-all
-ct / --clear-token
-o / --path  
```


## Project status
Project is currently lacking real world testing in larger environments. 
Watch out for the following:
 - management groups  
 - Administration Groups(ou)
 - Ratelimiting or Max Results on API