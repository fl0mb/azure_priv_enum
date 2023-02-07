import requests
import json
import time
import os.path
import argparse
import urllib.parse
import sys
import aiohttp
import asyncio
import platform

final_permissions = {}
apps = []
groups = []
group_owns = []
roleassignments = {}
global_subscriptions = []
pimtoken = ''

roledefinitions={'05352d14-a920-4328-a0de-4cbe7430e26b':'Azure Center for SAP solutions reader',
'aabbc5dd-1af0-458b-a942-81af88f9c138':'Azure Center for SAP solutions service role',
'7b0c7e81-271f-4c71-90bf-e30bdfdbc2f7':'Azure Center for SAP solutions administrator',
'fbc52c3f-28ad-4303-a892-8a056630b8f1':'Azure Traffic Controller Configuration Manager',
'4ba50f17-9666-485c-a643-ff00808643f0':'FHIR SMART User',
'a001fd3d-188f-4b5d-821b-7da978bf7442':'Cognitive Services OpenAI Contributor',
'5e0bd9bd-7b93-4f28-af87-19fc36ad61bd':'Cognitive Services OpenAI User',
'36e80216-a7e8-4f42-a7e1-f12c98cbaf8a':'Impact Reporter',
'68ff5d27-c7f5-4fa9-a21c-785d0df7bd9e':'Impact Reader',
'1afdec4b-e479-420e-99e7-f82237c7c5e6':'Azure Kubernetes Service Cluster Monitoring User',
'ad2dd5fb-cd4b-4fd4-a9b6-4fed3630980b':'ContainerApp Reader',
'f5819b54-e033-4d82-ac66-4fec3cbf3f4c':'Azure Connected Machine Resource Manager',
'8311e382-0749-4cb8-b61a-304f252e45ec':'AcrPush',
'312a565d-c81f-4fd8-895a-4e21e48d571c':'API Management Service Contributor',
'7f951dda-4ed3-4680-a7ca-43fe172d538d':'AcrPull',
'6cef56e8-d556-48e5-a04f-b8e64114680f':'AcrImageSigner',
'c2f4ef07-c644-48eb-af81-4b1b4947fb11':'AcrDelete',
'cdda3590-29a3-44f6-95f2-9f980659eb04':'AcrQuarantineReader',
'c8d4ff99-41c3-41a8-9f60-21dfdad59608':'AcrQuarantineWriter',
'e022efe7-f5ba-4159-bbe4-b44f577e9b61':'API Management Service Operator Role',
'71522526-b88f-4d52-b57f-d31fc3546d0d':'API Management Service Reader Role',
'ae349356-3a1b-4a5e-921d-050484c6347e':'Application Insights Component Contributor',
'08954f03-6346-4c2e-81c0-ec3a5cfae23b':'Application Insights Snapshot Debugger',
'fd1bd22b-8476-40bc-a0bc-69b95687b9f3':'Attestation Reader',
'4fe576fe-1146-4730-92eb-48519fa6bf9f':'Automation Job Operator',
'5fb5aef8-1081-4b8e-bb16-9d5d0385bab5':'Automation Runbook Operator',
'd3881f73-407a-4167-8283-e981cbba0404':'Automation Operator',
'4f8fab4f-1852-4a58-a46a-8eaf358af14a':'Avere Contributor',
'c025889f-8102-4ebf-b32c-fc0c6f0c6bd9':'Avere Operator',
'0ab0b1a8-8aac-4efd-b8c2-3ee1fb270be8':'Azure Kubernetes Service Cluster Admin Role',
'4abbcc35-e782-43d8-92c5-2d3f1bd2253f':'Azure Kubernetes Service Cluster User Role',
'423170ca-a8f6-4b0f-8487-9e4eb8f49bfa':'Azure Maps Data Reader',
'6f12a6df-dd06-4f3e-bcb1-ce8be600526a':'Azure Stack Registration Owner',
'5e467623-bb1f-42f4-a55d-6e525e11384b':'Backup Contributor',
'fa23ad8b-c56e-40d8-ac0c-ce449e1d2c64':'Billing Reader',
'00c29273-979b-4161-815c-10b084fb9324':'Backup Operator',
'a795c7a0-d4a2-40c1-ae25-d81f01202912':'Backup Reader',
'31a002a1-acaf-453e-8a5b-297c9ca1ea24':'Blockchain Member Node Access (Preview)',
'5e3c6656-6cfa-4708-81fe-0de47ac73342':'BizTalk Contributor',
'426e0c7f-0c7e-4658-b36f-ff54d6c29b45':'CDN Endpoint Contributor',
'871e35f6-b5c1-49cc-a043-bde969a0f2cd':'CDN Endpoint Reader',
'ec156ff8-a8d1-4d15-830c-5b80698ca432':'CDN Profile Contributor',
'8f96442b-4075-438f-813d-ad51ab4019af':'CDN Profile Reader',
'b34d265f-36f7-4a0d-a4d4-e158ca92e90f':'Classic Network Contributor',
'86e8f5dc-a6e9-4c67-9d15-de283e8eac25':'Classic Storage Account Contributor',
'985d6b00-f706-48f5-a6fe-d0ca12fb668d':'Classic Storage Account Key Operator Service Role',
'9106cda0-8a86-4e81-b686-29a22c54effe':'ClearDB MySQL DB Contributor',
'd73bb868-a0df-4d4d-bd69-98a00b01fccb':'Classic Virtual Machine Contributor',
'a97b65f3-24c7-4388-baec-2e87135dc908':'Cognitive Services User',
'b59867f0-fa02-499b-be73-45a86b5b3e1c':'Cognitive Services Data Reader (Preview)',
'25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68':'Cognitive Services Contributor',
'db7b14f2-5adf-42da-9f96-f2ee17bab5cb':'CosmosBackupOperator',
'b24988ac-6180-42a0-ab88-20f7382dd24c':'Contributor',
'fbdf93bf-df7d-467e-a4d2-9458aa1360c8':'Cosmos DB Account Reader Role',
'434105ed-43f6-45c7-a02f-909b2ba83430':'Cost Management Contributor',
'72fafb9e-0641-4937-9268-a91bfd8191a3':'Cost Management Reader',
'add466c9-e687-43fc-8d98-dfcf8d720be5':'Data Box Contributor',
'028f4ed7-e2a9-465e-a8f4-9c0ffdfdc027':'Data Box Reader',
'673868aa-7521-48a0-acc6-0f60742d39f5':'Data Factory Contributor',
'150f5e0c-0603-4f03-8c7f-cf70034c4e90':'Data Purger',
'47b7735b-770e-4598-a7da-8b91488b4c88':'Data Lake Analytics Developer',
'76283e04-6283-4c54-8f91-bcf1374a3c64':'DevTest Labs User',
'5bd9cd88-fe45-4216-938b-f97437e15450':'DocumentDB Account Contributor',
'befefa01-2a29-4197-83a8-272ff33ce314':'DNS Zone Contributor',
'428e0ff0-5e57-4d9c-a221-2c70d0e0a443':'EventGrid EventSubscription Contributor',
'2414bbcf-6497-4faf-8c65-045460748405':'EventGrid EventSubscription Reader',
'b60367af-1334-4454-b71e-769d9a4f83d9':'Graph Owner',
'8d8d5a11-05d3-4bda-a417-a08778121c7c':'HDInsight Domain Services Contributor',
'03a6d094-3444-4b3d-88af-7477090a9e5e':'Intelligent Systems Account Contributor',
'f25e0fa2-a7c8-4377-a976-54943a77a395':'Key Vault Contributor',
'ee361c5d-f7b5-4119-b4b6-892157c8f64c':'Knowledge Consumer',
'b97fb8bc-a8b2-4522-a38b-dd33c7e65ead':'Lab Creator',
'73c42c96-874c-492b-b04d-ab87d138a893':'Log Analytics Reader',
'92aaf0da-9dab-42b6-94a3-d43ce8d16293':'Log Analytics Contributor',
'515c2055-d9d4-4321-b1b9-bd0c9a0f79fe':'Logic App Operator',
'87a39d53-fc1b-424a-814c-f7e04687dc9e':'Logic App Contributor',
'c7393b34-138c-406f-901b-d8cf2b17e6ae':'Managed Application Operator Role',
'b9331d33-8a36-4f8c-b097-4f54124fdb44':'Managed Applications Reader',
'f1a07417-d97a-45cb-824c-7a7467783830':'Managed Identity Operator',
'e40ec5ca-96e0-45a2-b4ff-59039f2c2b59':'Managed Identity Contributor',
'5d58bcaf-24a5-4b20-bdb6-eed9f69fbe4c':'Management Group Contributor',
'ac63b705-f282-497d-ac71-919bf39d939d':'Management Group Reader',
'3913510d-42f4-4e42-8a64-420c390055eb':'Monitoring Metrics Publisher',
'43d0d8ad-25c7-4714-9337-8ba259a9fe05':'Monitoring Reader',
'4d97b98b-1d4f-4787-a291-c67834d212e7':'Network Contributor',
'749f88d5-cbae-40b8-bcfc-e573ddc772fa':'Monitoring Contributor',
'5d28c62d-5b37-4476-8438-e587778df237':'New Relic APM Account Contributor',
'8e3af657-a8ff-443c-a75c-2fe8c4bcb635':'Owner',
'acdd72a7-3385-48ef-bd42-f606fba81ae7':'Reader',
'e0f68234-74aa-48ed-b826-c38b57376e17':'Redis Cache Contributor',
'c12c1c16-33a1-487b-954d-41c89c60f349':'Reader and Data Access',
'36243c78-bf99-498c-9df9-86d9f8d28608':'Resource Policy Contributor',
'188a0f2f-5c9e-469b-ae67-2aa5ce574b94':'Scheduler Job Collections Contributor',
'7ca78c08-252a-4471-8644-bb5ff32d4ba0':'Search Service Contributor',
'fb1c8493-542b-48eb-b624-b4c8fea62acd':'Security Admin',
'e3d13bf0-dd5a-482e-ba6b-9b8433878d10':'Security Manager (Legacy)',
'39bc4728-0917-49c7-9d2c-d95423bc2eb4':'Security Reader',
'8bbe83f1-e2a6-4df7-8cb4-4e04d4e5c827':'Spatial Anchors Account Contributor',
'6670b86e-a3f7-4917-ac9b-5d6ab1be4567':'Site Recovery Contributor',
'494ae006-db33-4328-bf46-533a6560a3ca':'Site Recovery Operator',
'5d51204f-eb77-4b1c-b86a-2ec626c49413':'Spatial Anchors Account Reader',
'dbaa88c4-0c30-4179-9fb3-46319faa6149':'Site Recovery Reader',
'70bbe301-9835-447d-afdd-19eb3167307c':'Spatial Anchors Account Owner',
'4939a1f6-9ae0-4e48-a1e0-f2cbe897382d':'SQL Managed Instance Contributor',
'9b7fa17d-e63e-47b0-bb0a-15c516ac86ec':'SQL DB Contributor',
'056cd41c-7e88-42e1-933e-88ba6a50c9c3':'SQL Security Manager',
'17d1049b-9a84-46fb-8f53-869881c3d3ab':'Storage Account Contributor',
'6d8ee4ec-f05a-4a1d-8b00-a9b17e38b437':'SQL Server Contributor',
'81a9662b-bebf-436f-a333-f67b29880f12':'Storage Account Key Operator Service Role',
'ba92f5b4-2d11-453d-a403-e96b0029c9fe':'Storage Blob Data Contributor',
'b7e6dc6d-f1e8-4753-8033-0f276bb0955b':'Storage Blob Data Owner',
'2a2b9908-6ea1-4ae2-8e65-a410df84e7d1':'Storage Blob Data Reader',
'974c5e8b-45b9-4653-ba55-5f855dd0fb88':'Storage Queue Data Contributor',
'8a0f0c08-91a1-4084-bc3d-661d67233fed':'Storage Queue Data Message Processor',
'c6a89b2d-59bc-44d0-9896-0f6e12d7b80a':'Storage Queue Data Message Sender',
'19e7f393-937e-4f77-808e-94535e297925':'Storage Queue Data Reader',
'cfd33db0-3dd1-45e3-aa9d-cdbdf3b6f24e':'Support Request Contributor',
'a4b10055-b0c7-44c2-b00f-c7b5b3550cf7':'Traffic Manager Contributor',
'1c0163c0-47e6-4577-8991-ea5c82e286e4':'Virtual Machine Administrator Login',
'18d7d88d-d35e-4fb5-a5c3-7773c20a72d9':'User Access Administrator',
'fb879df8-f326-4884-b1cf-06f3ad86be52':'Virtual Machine User Login',
'9980e02c-c2be-4d73-94e8-173b1dc7cf3c':'Virtual Machine Contributor',
'2cc479cb-7b4d-49a8-b449-8c00fd0f0a4b':'Web Plan Contributor',
'de139f84-1756-47ae-9be6-808fbbe84772':'Website Contributor',
'090c5cfd-751d-490a-894a-3ce6f1109419':'Azure Service Bus Data Owner',
'f526a384-b230-433a-b45c-95f59c4a2dec':'Azure Event Hubs Data Owner',
'bbf86eb8-f7b4-4cce-96e4-18cddf81d86e':'Attestation Contributor',
'61ed4efc-fab3-44fd-b111-e24485cc132a':'HDInsight Cluster Operator',
'230815da-be43-4aae-9cb4-875f7bd000aa':'Cosmos DB Operator',
'48b40c6e-82e0-4eb3-90d5-19e40f49b624':'Hybrid Server Resource Administrator',
'5d1e5ee4-7c68-4a71-ac8b-0739630a3dfb':'Hybrid Server Onboarding',
'a638d3c7-ab3a-418d-83e6-5f17a39d4fde':'Azure Event Hubs Data Receiver',
'2b629674-e913-4c01-ae53-ef4638d8f975':'Azure Event Hubs Data Sender',
'4f6d3b9b-027b-4f4c-9142-0e5a2a2247e0':'Azure Service Bus Data Receiver',
'69a216fc-b8fb-44d8-bc22-1f3c2cd27a39':'Azure Service Bus Data Sender',
'aba4ae5f-2193-4029-9191-0cb91df5e314':'Storage File Data SMB Share Reader',
'0c867c2a-1d8c-454a-a3db-ab2ea1bdc8bb':'Storage File Data SMB Share Contributor',
'b12aa53e-6015-4669-85d0-8515ebb3ae7f':'Private DNS Zone Contributor',
'db58b8e5-c6ad-4a2a-8342-4190687cbf4a':'Storage Blob Delegator',
'1d18fff3-a72a-46b5-b4a9-0b38a3cd7e63':'Desktop Virtualization User',
'a7264617-510b-434b-a828-9731dc254ea7':'Storage File Data SMB Share Elevated Contributor',
'41077137-e803-4205-871c-5a86e6a753b4':'Blueprint Contributor',
'437d2ced-4a38-4302-8479-ed2bcb43d090':'Blueprint Operator',
'ab8e14d6-4a74-4a29-9ba8-549422addade':'Microsoft Sentinel Contributor',
'3e150937-b8fe-4cfb-8069-0eaf05ecd056':'Microsoft Sentinel Responder',
'8d289c81-5878-46d4-8554-54e1e3d8b5cb':'Microsoft Sentinel Reader',
'b279062a-9be3-42a0-92ae-8b3cf002ec4d':'Workbook Reader',
'e8ddcd69-c73f-4f9f-9844-4100522f16ad':'Workbook Contributor',
'66bb4e9e-b016-4a94-8249-4c0511c2be84':'Policy Insights Data Writer (Preview)',
'04165923-9d83-45d5-8227-78b77b0a687e':'SignalR AccessKey Reader',
'8cf5e20a-e4b2-4e9d-b3a1-5ceb692c2761':'SignalR/Web PubSub Contributor',
'b64e21ea-ac4e-4cdf-9dc9-5b892992bee7':'Azure Connected Machine Onboarding',
'cd570a14-e51a-42ad-bac8-bafd67325302':'Azure Connected Machine Resource Administrator',
'91c1777a-f3dc-4fae-b103-61d183457e46':'Managed Services Registration assignment Delete Role',
'5ae67dd6-50cb-40e7-96ff-dc2bfa4b606b':'App Configuration Data Owner',
'516239f1-63e1-4d78-a4de-a74fb236a071':'App Configuration Data Reader',
'34e09817-6cbe-4d01-b1a2-e0eac5743d41':'Kubernetes Cluster - Azure Arc Onboarding',
'7f646f1b-fa08-80eb-a22b-edd6ce5c915c':'Experimentation Contributor',
'466ccd10-b268-4a11-b098-b4849f024126':'Cognitive Services QnA Maker Reader',
'f4cc2bf9-21be-47a1-bdf1-5c5804381025':'Cognitive Services QnA Maker Editor',
'7f646f1b-fa08-80eb-a33b-edd6ce5c915c':'Experimentation Administrator',
'3df8b902-2a6f-47c7-8cc5-360e9b272a7e':'Remote Rendering Administrator',
'd39065c4-c120-43c9-ab0a-63eed9795f0a':'Remote Rendering Client',
'641177b8-a67a-45b9-a033-47bc880bb21e':'Managed Application Contributor Role',
'612c2aa1-cb24-443b-ac28-3ab7272de6f5':'Security Assessment Contributor',
'4a9ae827-6dc8-4573-8ac7-8239d42aa03f':'Tag Contributor',
'c7aa55d3-1abb-444a-a5ca-5e51e485d6ec':'Integration Service Environment Developer',
'a41e2c5b-bd99-4a07-88f4-9bf657a760b8':'Integration Service Environment Contributor',
'ed7f3fbd-7b88-4dd4-9017-9adb7ce333f8':'Azure Kubernetes Service Contributor Role',
'd57506d4-4c8d-48b1-8587-93c323f6a5a3':'Azure Digital Twins Data Reader',
'bcd981a7-7f74-457b-83e1-cceb9e632ffe':'Azure Digital Twins Data Owner',
'350f8d15-c687-4448-8ae1-157740a3936d':'Hierarchy Settings Administrator',
'5a1fc7df-4bf1-4951-a576-89034ee01acd':'FHIR Data Contributor',
'3db33094-8700-4567-8da5-1501d4e7e843':'FHIR Data Exporter',
'4c8d0bbc-75d3-4935-991f-5f3c56d81508':'FHIR Data Reader',
'3f88fce4-5892-4214-ae73-ba5294559913':'FHIR Data Writer',
'49632ef5-d9ac-41f4-b8e7-bbe587fa74a1':'Experimentation Reader',
'4dd61c23-6743-42fe-a388-d8bdd41cb745':'Object Understanding Account Owner',
'8f5e0ce6-4f7b-4dcf-bddf-e6f48634a204':'Azure Maps Data Contributor',
'c1ff6cc2-c111-46fe-8896-e0ef812ad9f3':'Cognitive Services Custom Vision Contributor',
'5c4089e1-6d96-4d2f-b296-c1bc7137275f':'Cognitive Services Custom Vision Deployment',
'88424f51-ebe7-446f-bc41-7fa16989e96c':'Cognitive Services Custom Vision Labeler',
'93586559-c37d-4a6b-ba08-b9f0940c2d73':'Cognitive Services Custom Vision Reader',
'0a5ae4ab-0d65-4eeb-be61-29fc9b54394b':'Cognitive Services Custom Vision Trainer',
'00482a5a-887f-4fb3-b363-3b7fe8e74483':'Key Vault Administrator',
'14b46e9e-c2b7-41b4-b07b-48a6ebf60603':'Key Vault Crypto Officer',
'12338af0-0e69-4776-bea7-57ae8d297424':'Key Vault Crypto User',
'b86a8fe4-44ce-4948-aee5-eccb2c155cd7':'Key Vault Secrets Officer',
'4633458b-17de-408a-b874-0445c86b69e6':'Key Vault Secrets User',
'a4417e6f-fecd-4de8-b567-7b0420556985':'Key Vault Certificates Officer',
'21090545-7ca7-4776-b22c-e363652d74d2':'Key Vault Reader',
'e147488a-f6f5-4113-8e2d-b22465e65bf6':'Key Vault Crypto Service Encryption User',
'63f0a09d-1495-4db4-a681-037d84835eb4':'Azure Arc Kubernetes Viewer',
'5b999177-9696-4545-85c7-50de3797e5a1':'Azure Arc Kubernetes Writer',
'8393591c-06b9-48a2-a542-1bd6b377f6a2':'Azure Arc Kubernetes Cluster Admin',
'dffb1e0c-446f-4dde-a09f-99eb5cc68b96':'Azure Arc Kubernetes Admin',
'b1ff04bb-8a4e-4dc4-8eb5-8693973ce19b':'Azure Kubernetes Service RBAC Cluster Admin',
'3498e952-d568-435e-9b2c-8d77e338d7f7':'Azure Kubernetes Service RBAC Admin',
'7f6c6a51-bcf8-42ba-9220-52d62157d7db':'Azure Kubernetes Service RBAC Reader',
'a7ffa36f-339b-4b5c-8bdf-e2c188b2c0eb':'Azure Kubernetes Service RBAC Writer',
'82200a5b-e217-47a5-b665-6d8765ee745b':'Services Hub Operator',
'd18777c0-1514-4662-8490-608db7d334b6':'Object Understanding Account Reader',
'00493d72-78f6-4148-b6c5-d3ce8e4799dd':'Azure Arc Enabled Kubernetes Cluster User Role',
'420fcaa2-552c-430f-98ca-3264be4806c7':'SignalR App Server',
'fd53cd77-2268-407a-8f46-7e7863d0f521':'SignalR REST API Owner',
'daa9e50b-21df-454c-94a6-a8050adab352':'Collaborative Data Contributor',
'e9dba6fb-3d52-4cf0-bce3-f06ce71b9e0f':'Device Update Reader',
'02ca0879-e8e4-47a5-a61e-5c618b76e64a':'Device Update Administrator',
'0378884a-3af5-44ab-8323-f5b22f9f3c98':'Device Update Content Administrator',
'e4237640-0e3d-4a46-8fda-70bc94856432':'Device Update Deployments Administrator',
'49e2f5d2-7741-4835-8efa-19e1fe35e47f':'Device Update Deployments Reader',
'd1ee9a80-8b14-47f0-bdc2-f4a351625a7b':'Device Update Content Reader',
'cb43c632-a144-4ec5-977c-e80c4affc34a':'Cognitive Services Metrics Advisor Administrator',
'3b20f47b-3825-43cb-8114-4bd2201156a8':'Cognitive Services Metrics Advisor User',
'2c56ea50-c6b3-40a6-83c0-9d98858bc7d2':'Schema Registry Reader (Preview)',
'5dffeca3-4936-4216-b2bc-10343a5abb25':'Schema Registry Contributor (Preview)',
'7ec7ccdc-f61e-41fe-9aaf-980df0a44eba':'AgFood Platform Service Reader',
'8508508a-4469-4e45-963b-2518ee0bb728':'AgFood Platform Service Contributor',
'f8da80de-1ff9-4747-ad80-a19b7f6079e3':'AgFood Platform Service Admin',
'18500a29-7fe2-46b2-a342-b16a415e101d':'Managed HSM contributor',
'0b555d9b-b4a7-4f43-b330-627f0e5be8f0':'Security Detonation Chamber Submitter',
'ddde6b66-c0df-4114-a159-3618637b3035':'SignalR REST API Reader',
'7e4f1700-ea5a-4f59-8f37-079cfe29dce3':'SignalR Service Owner',
'f7b75c60-3036-4b75-91c3-6b41c27c1689':'Reservation Purchaser',
'635dd51f-9968-44d3-b7fb-6d9a6bd613ae':'AzureML Metrics Writer (preview)',
'e5e2a7ff-d759-4cd2-bb51-3152d37e2eb1':'Storage Account Backup Contributor',
'6188b7c9-7d01-4f99-a59f-c88b630326c0':'Experimentation Metric Contributor',
'9ef4ef9c-a049-46b0-82ab-dd8ac094c889':'Project Babylon Data Curator',
'c8d896ba-346d-4f50-bc1d-7d1c84130446':'Project Babylon Data Reader',
'05b7651b-dc44-475e-b74d-df3db49fae0f':'Project Babylon Data Source Administrator',
'8a3c2885-9b38-4fd2-9d99-91af537c1347':'Purview role 1 (Deprecated)',
'ff100721-1b9d-43d8-af52-42b69c1272db':'Purview role 3 (Deprecated)',
'200bba9e-f0c8-430f-892b-6f0794863803':'Purview role 2 (Deprecated)',
'ca6382a4-1721-4bcf-a114-ff0c70227b6b':'Application Group Contributor',
'49a72310-ab8d-41df-bbb0-79b649203868':'Desktop Virtualization Reader',
'082f0a83-3be5-4ba1-904c-961cca79b387':'Desktop Virtualization Contributor',
'21efdde3-836f-432b-bf3d-3e8e734d4b2b':'Desktop Virtualization Workspace Contributor',
'ea4bfff8-7fb4-485a-aadd-d4129a0ffaa6':'Desktop Virtualization User Session Operator',
'2ad6aaab-ead9-4eaa-8ac5-da422f562408':'Desktop Virtualization Session Host Operator',
'ceadfde2-b300-400a-ab7b-6143895aa822':'Desktop Virtualization Host Pool Reader',
'e307426c-f9b6-4e81-87de-d99efb3c32bc':'Desktop Virtualization Host Pool Contributor',
'aebf23d0-b568-4e86-b8f9-fe83a2c6ab55':'Desktop Virtualization Application Group Reader',
'86240b0e-9422-4c43-887b-b61143f32ba8':'Desktop Virtualization Application Group Contributor',
'0fa44ee9-7a7d-466b-9bb2-2bf446b1204d':'Desktop Virtualization Workspace Reader',
'3e5e47e6-65f7-47ef-90b5-e5dd4d455f24':'Disk Backup Reader',
'b8b15564-4fa6-4a59-ab12-03e1d9594795':'Autonomous Development Platform Data Contributor (Preview)',
'd63b75f7-47ea-4f27-92ac-e0d173aaf093':'Autonomous Development Platform Data Reader (Preview)',
'27f8b550-c507-4db9-86f2-f4b8e816d59d':'Autonomous Development Platform Data Owner (Preview)',
'b50d9833-a0cb-478e-945f-707fcc997c13':'Disk Restore Operator',
'7efff54f-a5b4-42b5-a1c5-5411624893ce':'Disk Snapshot Contributor',
'5548b2cf-c94c-4228-90ba-30851930a12f':'Microsoft.Kubernetes connected cluster role',
'a37b566d-3efa-4beb-a2f2-698963fa42ce':'Security Detonation Chamber Submission Manager',
'352470b3-6a9c-4686-b503-35deb827e500':'Security Detonation Chamber Publisher',
'7a6f0e70-c033-4fb1-828c-08514e5f4102':'Collaborative Runtime Operator',
'5432c526-bc82-444a-b7ba-57c5b0b5b34f':'CosmosRestoreOperator',
'a1705bd2-3a8f-45a5-8683-466fcfd5cc24':'FHIR Data Converter',
'f4c81013-99ee-4d62-a7ee-b3f1f648599a':'Microsoft Sentinel Automation Contributor',
'0e5f05e5-9ab9-446b-b98d-1e2157c94125':'Quota Request Operator',
'1e241071-0855-49ea-94dc-649edcd759de':'EventGrid Contributor',
'28241645-39f8-410b-ad48-87863e2951d5':'Security Detonation Chamber Reader',
'4a167cdf-cb95-4554-9203-2347fe489bd9':'Object Anchors Account Reader',
'ca0835dd-bacc-42dd-8ed2-ed5e7230d15b':'Object Anchors Account Owner',
'd17ce0a2-0697-43bc-aac5-9113337ab61c':'WorkloadBuilder Migration Agent Role',
'12cf5a90-567b-43ae-8102-96cf46c7d9b4':'Web PubSub Service Owner (Preview)',
'bfb1c7d2-fb1a-466b-b2ba-aee63b92deaf':'Web PubSub Service Reader (Preview)',
'b5537268-8956-4941-a8f0-646150406f0c':'Azure Spring Cloud Data Reader',
'f2dc8367-1007-4938-bd23-fe263f013447':'Cognitive Services Speech User',
'0e75ca1e-0464-4b4d-8b93-68208a576181':'Cognitive Services Speech Contributor',
'9894cab4-e18a-44aa-828b-cb588cd6f2d7':'Cognitive Services Face Recognizer',
'054126f8-9a2b-4f1c-a9ad-eca461f08466':'Media Services Account Administrator',
'532bc159-b25e-42c0-969e-a1d439f60d77':'Media Services Live Events Administrator',
'e4395492-1534-4db2-bedf-88c14621589c':'Media Services Media Operator',
'c4bba371-dacd-4a26-b320-7250bca963ae':'Media Services Policy Administrator',
'99dba123-b5fe-44d5-874c-ced7199a5804':'Media Services Streaming Endpoints Administrator',
'1ec5b3c1-b17e-4e25-8312-2acb3c3c5abf':'Stream Analytics Query Tester',
'a2138dac-4907-4679-a376-736901ed8ad8':'AnyBuild Builder',
'b447c946-2db7-41ec-983d-d8bf3b1c77e3':'IoT Hub Data Reader',
'494bdba2-168f-4f31-a0a1-191d2f7c028c':'IoT Hub Twin Contributor',
'4ea46cd5-c1b2-4a8e-910b-273211f9ce47':'IoT Hub Registry Contributor',
'4fc6c259-987e-4a07-842e-c321cc9d413f':'IoT Hub Data Contributor',
'15e0f5a1-3450-4248-8e25-e2afe88a9e85':'Test Base Reader',
'1407120a-92aa-4202-b7e9-c0e197c71c8f':'Search Index Data Reader',
'8ebe5a00-799e-43f5-93ac-243d3dce84a7':'Search Index Data Contributor',
'76199698-9eea-4c19-bc75-cec21354c6b6':'Storage Table Data Reader',
'0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3':'Storage Table Data Contributor',
'e89c7a3c-2f64-4fa1-a847-3e4c9ba4283a':'DICOM Data Reader',
'58a3b984-7adf-4c20-983a-32417c86fbc8':'DICOM Data Owner',
'd5a91429-5739-47e2-a06b-3470a27159e7':'EventGrid Data Sender',
'60fc6e62-5479-42d4-8bf4-67625fcc2840':'Disk Pool Operator',
'f6c7c914-8db3-469d-8ca1-694a8f32e121':'AzureML Data Scientist',
'22926164-76b3-42b3-bc55-97df8dab3e41':'Grafana Admin',
'e8113dce-c529-4d33-91fa-e9b972617508':'Azure Connected SQL Server Onboarding',
'26baccc8-eea7-41f1-98f4-1762cc7f685d':'Azure Relay Sender',
'2787bf04-f1f5-4bfe-8383-c8a24483ee38':'Azure Relay Owner',
'26e0b698-aa6d-4085-9386-aadae190014d':'Azure Relay Listener',
'60921a7e-fef1-4a43-9b16-a26c52ad4769':'Grafana Viewer',
'a79a5197-3a5c-4973-a920-486035ffd60f':'Grafana Editor',
'f353d9bd-d4a6-484e-a77a-8050b599b867':'Automation Contributor',
'85cb6faf-e071-4c9b-8136-154b5a04f717':'Kubernetes Extension Contributor',
'10745317-c249-44a1-a5ce-3a4353c0bbd8':'Device Provisioning Service Data Reader',
'dfce44e4-17b7-4bd1-a6d1-04996ec95633':'Device Provisioning Service Data Contributor',
'2837e146-70d7-4cfd-ad55-7efa6464f958':'Code Signing Certificate Profile Signer',
'cff1b556-2399-4e7e-856d-a8f754be7b65':'Azure Spring Cloud Service Registry Reader',
'f5880b48-c26d-48be-b172-7927bfa1c8f1':'Azure Spring Cloud Service Registry Contributor',
'd04c6db6-4947-4782-9e91-30a88feb7be7':'Azure Spring Cloud Config Server Reader',
'a06f5c24-21a7-4e1a-aa2b-f19eb6684f5b':'Azure Spring Cloud Config Server Contributor',
'6ae96244-5829-4925-a7d3-5975537d91dd':'Azure VM Managed identities restore Contributor',
'6be48352-4f82-47c9-ad5e-0acacefdb005':'Azure Maps Search and Render Data Reader',
'dba33070-676a-4fb0-87fa-064dc56ff7fb':'Azure Maps Contributor',
'b748a06d-6150-4f8a-aaa9-ce3940cd96cb':'Azure Arc VMware VM Contributor',
'ce551c02-7c42-47e0-9deb-e3b6fc3a9a83':'Azure Arc VMware Private Cloud User',
'ddc140ed-e463-4246-9145-7c664192013f':'Azure Arc VMware Administrator role ',
'67d33e57-3129-45e6-bb0b-7cc522f762fa':'Azure Arc VMware Private Clouds Onboarding',
'f72c8140-2111-481c-87ff-72b910f6e3f8':'Cognitive Services LUIS Owner',
'7628b7b8-a8b2-4cdc-b46f-e9b35248918e':'Cognitive Services Language Reader',
'f2310ca1-dc64-4889-bb49-c8e0fa3d47a8':'Cognitive Services Language Writer',
'f07febfe-79bc-46b1-8b37-790e26e6e498':'Cognitive Services Language Owner',
'18e81cdc-4e98-4e29-a639-e7d10c5a6226':'Cognitive Services LUIS Reader',
'6322a993-d5c9-4bed-b113-e49bbea25b27':'Cognitive Services LUIS Writer',
'a9a19cc5-31f4-447c-901f-56c0bb18fcaf':'PlayFab Reader',
'749a398d-560b-491b-bb21-08924219302e':'Load Test Contributor',
'45bb0b16-2f0c-4e78-afaa-a07599b003f6':'Load Test Owner',
'0c8b84dc-067c-4039-9615-fa1a4b77c726':'PlayFab Contributor',
'3ae3fb29-0000-4ccd-bf80-542e7b26e081':'Load Test Reader',
'b2de6794-95db-4659-8781-7e080d3f2b9d':'Cognitive Services Immersive Reader User',
'f69b8690-cc87-41d6-b77a-a4bc3c0a966f':'Lab Services Contributor',
'2a5c394f-5eb7-4d4f-9c8e-e8eae39faebc':'Lab Services Reader',
'ce40b423-cede-4313-a93f-9b28290b72e1':'Lab Assistant',
'a36e6959-b6be-4b12-8e9f-ef4b474d304d':'Lab Operator',
'5daaa2af-1fe8-407c-9122-bba179798270':'Lab Contributor',
'4447db05-44ed-4da3-ae60-6cbece780e32':'Chamber User',
'4e9b8407-af2e-495b-ae54-bb60a55b1b5a':'Chamber Admin',
'a6333a3e-0164-44c3-b281-7a577aff287f':'Windows Admin Center Administrator Login',
'088ab73d-1256-47ae-bea9-9de8e7131f31':'Guest Configuration Resource Contributor',
'18ed5180-3e48-46fd-8541-4ea054d57064':'Azure Kubernetes Service Policy Add-on Deployment',
'361898ef-9ed1-48c2-849c-a832951106bb':'Domain Services Reader',
'eeaeda52-9324-47f6-8069-5d5bade478b2':'Domain Services Contributor',
'0f2ebee7-ffd4-4fc0-b3b7-664099fdad5d':'DNS Resolver Contributor',
'959f8984-c045-4866-89c7-12bf9737be2e':'Data Operator for Managed Disks',
'6b77f0a0-0d89-41cc-acd1-579c22c17a67':'AgFood Platform Sensor Partner Contributor',
'1ef6a3be-d0ac-425d-8c01-acb62866290b':'Compute Gallery Sharing Admin',
'cd08ab90-6b14-449c-ad9a-8f8e549482c6':'Scheduled Patching Contributor',
'45d50f46-0b78-4001-a660-4198cbe8cd05':'DevCenter Dev Box User',
'331c37c6-af14-46d9-b9f4-e1909e1b95a0':'DevCenter Project Admin',
'602da2ba-a5c2-41da-b01d-5360126ab525':'Virtual Machine Local User Login',
'e582369a-e17b-42a5-b10c-874c387c530b':'Azure Arc ScVmm VM Contributor',
'6aac74c4-6311-40d2-bbdd-7d01e7c6e3a9':'Azure Arc ScVmm Private Clouds Onboarding',
'c0781e91-8102-4553-8951-97c6d4243cda':'Azure Arc ScVmm Private Cloud User',
'a92dfd61-77f9-4aec-a531-19858b406c87':'Azure Arc ScVmm Administrator role',
'4465e953-8ced-4406-a58e-0f6e3f3b530b':'FHIR Data Importer',
'c031e6a8-4391-4de0-8d69-4706a7ed3729':'API Management Developer Portal Content Editor',
'd24ecba3-c1f4-40fa-a7bb-4588a071e8fd':'VM Scanner Operator',
'80dcbedb-47ef-405d-95bd-188a1b4ac406':'Elastic SAN Owner',
'af6a70f8-3c9f-4105-acf1-d719e9fca4ca':'Elastic SAN Reader',
'489581de-a3bd-480d-9518-53dea7416b33':'Desktop Virtualization Power On Contributor',
'a959dbd1-f747-45e3-8ba6-dd80f235f97c':'Desktop Virtualization Virtual Machine Contributor',
'40c5ff49-9181-41f8-ae61-143b0e78555e':'Desktop Virtualization Power On Off Contributor',
'a8281131-f312-4f34-8d98-ae12be9f0d23':'Elastic SAN Volume Group Owner',
'76cc9ee4-d5d3-4a45-a930-26add3d73475':'Access Review Operator Service Role',
'4339b7cf-9826-4e41-b4ed-c7f4505dac08':'Code Signing Identity Verifier',
'a2c4a527-7dc0-4ee3-897b-403ade70fafb':'Video Indexer Restricted Viewer',
'b0d8363b-8ddd-447d-831f-62ca05bff136':'Monitoring Data Reader',
'63bb64ad-9799-4770-b5c3-24ed299a07bf':'Azure Kubernetes Fleet Manager Contributor Role',
'5af6afb3-c06c-4fa4-8848-71a8aee05683':'Azure Kubernetes Fleet Manager RBAC Writer',
'434fb43a-c01c-447e-9f67-c3ad923cfaba':'Azure Kubernetes Fleet Manager RBAC Admin',
'18ab4d3d-a1bf-4477-8ad9-8359bc988f69':'Azure Kubernetes Fleet Manager RBAC Cluster Admin',
'30b27cfc-9c84-438e-b0ce-70e35255df80':'Azure Kubernetes Fleet Manager RBAC Reader',
'ba79058c-0414-4a34-9e42-c3399d80cd5a':'Kubernetes Namespace User',
'c6decf44-fd0a-444c-a844-d653c394e7ab':'Data Labeling - Labeler',
'f58310d9-a9f6-439a-9e8d-f62e7b41a168':'Role Based Access Control Administrator (Preview)',
'392ae280-861d-42bd-9ea5-08ee6d83b80e':'Template Spec Reader',
'1c9b6475-caf0-4164-b5a1-2142a7116f4b':'Template Spec Contributor',
'51d6186e-6489-4900-b93f-92e23144cca5':'Microsoft Sentinel Playbook Operator',
'18e40d4e-8d2e-438d-97e1-9528336e149c':'Deployment Environments User',
'80558df3-64f9-4c0f-b32d-e5094b036b0b':'Azure Spring Apps Connect Role',
'a99b0159-1064-4c22-a57b-c9b3caa1c054':'Azure Spring Apps Remote Debugging Role',
'e503ece1-11d0-4e8e-8e2c-7a6c3bf38815':'AzureML Compute Operator',
'1823dd4f-9b8c-4ab6-ab4e-7397a3684615':'AzureML Registry User'}

async def url_helper_get(session , url):
    async with session.get(url) as resp:
        if resp.status != 200:
            print('ERROR (url_helper_get):\n')
            error = await resp.text()
            print (error)
        else:
            out = await resp.json()
            return(out)

async def url_helper_post(session , url, json):
    async with session.post(url, json) as resp:
        if resp.status != 200:
            print('ERROR (url_helper_post):\n')
            error = await resp.text()
            print (error)
        else:
            out = await resp.json()
            return(out)

def devicecodeflow(tenantid):
    
    # old but stil works
    #body = {'client_id': '1950a258-227b-4e31-a9cf-717495945fc2', 'resource': 'https://management.azure.com/'}
    #response = requests.post('https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0' , data=body)
    
    #both would work:
    #https://management.azure.com/.default
    #https://management.azure.com/user_impersonation

    if os.path.exists('token.json'):
        file = open('token.json', 'r')
        tokens=json.load(file)
    else:
        body = {'client_id': '1950a258-227b-4e31-a9cf-717495945fc2', 'scope': 'https://management.azure.com/.default offline_access'}
        path = 'https://login.microsoftonline.com/'+ tenantid +'/oauth2/v2.0/devicecode'
        response = requests.post(path , data=body)
        #Show user the login message
        if response.status_code != 200:
            print('ERROR:\n' + response.text)
        else:
            data =response.json()
            print(data['message'])

        #wait for the users login
        time.sleep(10)
        body={'client_id':'1950a258-227b-4e31-a9cf-717495945fc2','grant_type':'urn:ietf:params:oauth:grant-type:device_code','code':data['device_code']}
        for x in range(10):  
            path = 'https://login.microsoftonline.com/'+ tenantid +'/oauth2/v2.0/token'
            response = requests.post(path, data=body)
            if response.status_code == 200:
                break
            else:
                time.sleep(2)
        data=response.json()
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        tokens = {'access_token':access_token,'refresh_token':refresh_token}
        #save to disk
        file = open("token.json", "w")  
        json.dump(tokens, file)  
        file.close() 

    return tokens

async def refreshtoken(scope,refresh_token,tenantid):

    body={'scope':scope,'client_id':'1950a258-227b-4e31-a9cf-717495945fc2','grant_type':'refresh_token','refresh_token':refresh_token}

    async with aiohttp.ClientSession() as session:
        async with session.post('https://login.microsoftonline.com/'+tenantid+'/oauth2/v2.0/token', data=body) as resp:
            if resp.status != 200:
                print('ERROR (refreshtoken):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()
                access_token = data['access_token']
                refresh_token = data['refresh_token']
                tokens = {'access_token':access_token,'refresh_token':refresh_token}
                return tokens

async def get_resources(access_token):  
    global roleassignments  
    resources = []    
    subscriptions={}   
    headers={'Authorization': 'Bearer '+access_token}
    async with aiohttp.ClientSession(headers=headers) as session:

        for i in global_subscriptions:
            resourcegroups = []  
            async with session.get("https://management.azure.com/subscriptions/" + i +"/resourcegroups?api-version=2021-04-01") as resp:
                if resp.status != 200:
                    print('ERROR (get_resources2):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data2 = await resp.json()                      
                    for y in data2['value']:   
                    #create the list of resource groups         
                        resourcegroups.append(y['name'])
                        #append list of resource groups to subscriptions dict
                    subscriptions[i]=resourcegroups

        resource_urls = []        
        resource_roles_urls = []

        # create url list for combinations of subscriptions and resource groups
        for i in subscriptions:
            for y in subscriptions[i]: 
                resource_urls.append("https://management.azure.com/subscriptions/" + i + "/resourcegroups/" + y + "/resources?api-version=2022-06-01")               
               
    # get urls in the list concurrently
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i in resource_urls:
            tasks.append(asyncio.ensure_future(url_helper_get(session , i)))
        
        out = await asyncio.gather(*tasks)
        for response in out:
            for i in response['value']:
                # the id vlaue includes a full path and not just the object-id eg; /subscriptions/<subscription-id>/resourceGroups/prod/providers/Microsoft.Compute/disks/Hostname_OsDisk_1_0eed51d6146f44sjghfkjsfb550444f091
                resources.append(i['id'])

        # create url list for individual resources
        for i in resources:
            resource_roles_urls.append("https://management.azure.com" + i + "/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01")

        # get role assignments for individual resources. This will include all assignments from higher levels like management group or subscriptions due to inheritance.
        tasks = []
        for i in resource_roles_urls:
            tasks.append(asyncio.ensure_future(url_helper_get(session , i)))
        
        out = await asyncio.gather(*tasks)
        for response in out:
            for z in response['value']: 
                # create a Dictonary with the necessary details
                subdict = {}                
                subdict['scope'] = z['properties']['scope']
                #avoid long role definitionid
                text = z['properties']['roleDefinitionId']
                out=text.rsplit('/',1)
                subdict['roleDefinitionId'] = out[1]
                subdict['principalId'] = z['properties']['principalId']
                subdict['principalType'] = z['properties']['principalType']                
                # append the dictonary 
                roleassignments[z['name']] = subdict 


    #return roleassignments
    #save to disk
    # file = open("roleassignments.json", "w")  
    # json.dump(roleassignments, file)  
    # file.close()  

async def get_subscriptions(access_token):

    headers={'Authorization': 'Bearer '+access_token}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('https://management.azure.com/subscriptions?api-version=2020-01-01') as resp:
            if resp.status != 200:
                print('ERROR (refreshtoken):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()
                for i in data['value']:
                    global_subscriptions.append(i['subscriptionId'])

async def get_classic_admins(access_token, object_id, graph_token):
    # get classic administrators
    assignments = {}
    classic_admins = []

    # classic administrators are assigned via the email adress/ this created issues for guest users
    headers ={'Authorization': 'Bearer '+graph_token}
    path = 'https://graph.microsoft.com/v1.0/users/' + object_id
    async with aiohttp.ClientSession(headers=headers) as session:        
        async with session.get(path) as resp:
            if resp.status != 200:
                print('ERROR (get_classic_admins):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()
                test=data['userPrincipalName'].split("#EXT#")
                # only true for guest users
                if len(test) >= 2:
                    # recreate the actual email adress from azures #EXT# guest schema
                    email=test[0].replace('_','@')
                else:
                    email=data['userPrincipalName']


    headers={'Authorization': 'Bearer '+access_token}
  
    #for each subscription find classic admins
    #generate list of urls and then execute then concurrently
    subscriptions_list = []
    for i in global_subscriptions:  
        subscriptions_list.append('https://management.azure.com/subscriptions/' + i + '/providers/Microsoft.Authorization/classicAdministrators?api-version=2015-07-01')

    async with aiohttp.ClientSession(headers=headers) as session:    
        tasks = []
        for i in subscriptions_list:
            tasks.append(asyncio.ensure_future(url_helper_get(session , i)))    
        out = await asyncio.gather(*tasks)
        for response in out:
            for y in response['value']:
                assignments = {}
                if y['properties']['emailAddress'] == email:
                    assignments['emailAddress'] = y['properties']['emailAddress']
                    assignments['role'] = y['properties']['role']
                    classic_admins.append(assignments)
    
    return classic_admins
    
async def get_azurerm_roles(roleassignments,objectId,roledefinitions,access_token):
    azurerm_roles = []
    # fix naming
    for i in roleassignments:  
        for x in roledefinitions:  
            if roleassignments[i]['roleDefinitionId'] == x: 
                roleassignments[i]['roleDefinitionId']=roledefinitions[x]
    
    for i in roleassignments:
        #search for direct assignments
        if roleassignments[i]['principalId'] == objectId:
            assignments = {}
            assignments['Scope'] = roleassignments[i]['scope']
            assignments['Principal'] = await getnamebyid_noprint(roleassignments[i]['principalId'],access_token)
            assignments['Role'] = roleassignments[i]['roleDefinitionId']
            azurerm_roles.append(assignments)
    return azurerm_roles

def role_definitions(access_token):
    """old function currently unused because most role definitions are already included"""
    headers={'Authorization': 'Bearer '+access_token}
    #get subscriptions
    r=requests.get("https://management.azure.com/subscriptions?api-version=2020-01-01",headers=headers)
    if r.status_code != 200:
        print('ERROR:\n' + r.text)
    else:
        data=r.json()  
        roledefinitions={}  
        for i in data['value']: 
            #get role definitions on subscription level / (might not include all as they could exist on RG or resource level only) 
            path= 'https://management.azure.com/subscriptions/' + i['subscriptionId'] + '/providers/Microsoft.Authorization/roleDefinitions?api-version=2022-04-01'
            r = requests.get(path,headers=headers)
            if r.status_code != 200:
                print('ERROR:\n' + r.text)
            else:
                data2=r.json()
                for x in data2['value']:
                    roledefinitions[x['name']]=x['properties']['roleName']
    
    return roledefinitions

async def get_group_memberships(objectid , access_token, type):
    """gets all group memberships of a principal"""

    headers={'Authorization': 'Bearer '+access_token}
    async with aiohttp.ClientSession(headers=headers) as session:

        if type == 'user':    
            path ='https://graph.microsoft.com/v1.0/users/' + objectid + '/transitiveMemberOf'
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (get_group_memberships1):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        if i['@odata.type'] == "#microsoft.graph.group":
                            groups.append(i['id'])  
    
        elif type == 'servicePrincipal':        
            path ='https://graph.microsoft.com/v1.0/servicePrincipals/' + objectid + '/transitiveMemberOf'
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (get_group_memberships2):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        if i['@odata.type'] == "#microsoft.graph.group":
                            groups.append(i['id']) 

        # this step is needed for the transitive memberships
        elif type == 'group':  
            groups.append(objectid)

        # also get transitive groups e.g. if a group is member of another group
        urllist = []
        for y in groups:
            urllist.append('https://graph.microsoft.com/v1.0/groups/' + y+ '/transitiveMemberOf')
        tasks = []
        # request concurently
        for i in urllist:
            tasks.append(asyncio.ensure_future(url_helper_get(session , i)))        
        out = await asyncio.gather(*tasks)

        for response in out:
            #if response is empty there are no nested groups
            if response['value'] !='[]':
                #add the transitive group too
                #transitiveMemberOf does not only list groups / filtering is needed
                for x in response['value']:                   
                    if (x['@odata.type'] == '#microsoft.graph.group') and (x['id'] not in groups):
                        groups.append(x['id']) 

async def getnamebyid(objectid , access_token):

    headers = {'Authorization':'Bearer ' + access_token}
    path = 'https://graph.microsoft.com/v1.0/directoryObjects/getByIds'    
    body = {'ids':[objectid]}    

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(path, json = body) as resp:
            if resp.status != 200:
                print('ERROR (getnamebyid1):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()
                if data['value']:
                    for i in data['value']:
                        if 'userPrincipalName' in i:
                            print('\nUserPrincipalName: ' + i['userPrincipalName'])
                        if 'servicePrincipalType' in i:
                            print('\nServicePrincipalType: ' + i['servicePrincipalType'])
                        #appId = client-id
                        if 'appId' in i:
                            print('\nClient-Id: ' + i['appId'])
                        #get group name
                        if i['@odata.type'] == '#microsoft.graph.group':
                            print('\nGroup: ' + i['displayName'])
                        print('Type: ' + i['@odata.type'])
                        return objectid
                else:
                    #first request finds all types of directory objects. If empty however the user might have searched a client-id instead
                    path = "(appId='" + objectid + "')"
                    path = 'https://graph.microsoft.com/v1.0/servicePrincipals'+path                    
                    async with session.get(path) as resp:
                        if resp.status != 200:
                            print('ERROR (getnamebyid2):\n')
                            error = await resp.text()
                            print (error)
                        else:
                            data = await resp.json()
                            print('\nObject-Id: ' + data['id'])
                            print('ServicePrincipalType: ' + data['servicePrincipalType'])
                            print('Client-Id: ' + data['appId'])                            
                            # in case the user queried a client-id return a object id 
                            if data['id']: 
                                return data['id']
                
async def getnamebyid_noprint(objectid , access_token):
    headers = {'Authorization':'Bearer ' + access_token}
    path = 'https://graph.microsoft.com/v1.0/directoryObjects/getByIds'
    body = {'ids':[objectid]}    

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(path, json = body) as resp:
            if resp.status != 200:
                print('ERROR (getnamebyid_noprint):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()
                out = ''
                if data['value']:
                    for i in data['value']:
                        if 'userPrincipalName' in i:
                            out = i['userPrincipalName']
                        if 'servicePrincipalType' in i:
                            out = objectid +' (ServicePrincipal)'
                        #get group name
                        if i['@odata.type'] == '#microsoft.graph.group':
                            out = i['displayName'] +' (Group)'
                        return out

async def gettype(objectid , access_token):
    out = ''
    headers = {'Authorization':'Bearer ' + access_token}
    path = 'https://graph.microsoft.com/v1.0/directoryObjects/getByIds'
    body = {'ids':[objectid]}    
    async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(path, json = body) as resp:
                if resp.status != 200:
                    print('ERROR (gettype):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    if data['value']:
                        for i in data['value']:
                            if i['@odata.type'] == '#microsoft.graph.group':
                                out = 'group'
                            elif i['@odata.type'] == '#microsoft.graph.application':
                                out = 'application'
                            elif i['@odata.type'] == '#microsoft.graph.servicePrincipal':
                                out = 'servicePrincipal'
                            elif i['@odata.type'] == '#microsoft.graph.user':
                                out = 'user'
                    return out

async def getidbyname(name , access_token):
    headers = {'Authorization':'Bearer ' + access_token}
    name = urllib.parse.quote_plus(name)
    name = "('" + name + "')"
    path = 'https://graph.microsoft.com/v1.0/users' + name

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(path) as resp:
            if resp.status != 200:
                print('ERROR (getidbyname):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()
    return data['id']

def clearall():
    if os.path.exists('roleassignments.json'):
        os.remove("roleassignments.json")
    if os.path.exists('token.json'):
        os.remove("token.json")

def cleartoken():
    if os.path.exists('token.json'):
        os.remove("token.json")

async def output(final_permissions):
# there will be a better way to do this
    for i in final_permissions:
        if i == 'direct':
            print('\nDirect privileges of the given principal:')
            if final_permissions[i]['azuread_roles']:
                for x in final_permissions[i]['azuread_roles']:
                    print('\n\tAzureAD Role Assignment:')
                    print('\tRole: ' + x['Role'])
            if final_permissions[i]['azurerm_roles']:
                for x in final_permissions[i]['azurerm_roles']:
                    print('\n\tAzureRM Role Assignment:')
                    print('\tRole: ' + x['Role'])
                    print('\tScope: ' + x['Scope'])
                    print('\tPrincipal: ' + x['Principal'])                    
            if final_permissions[i]['classic_admins']:
                for x in final_permissions[i]['classic_admins']:
                    print('\n\tClassic Administrator Role Assignment:')
                    print('\tRole: ' + x['role'])
                    print('\tEmailAddress: ' + x['emailAddress'])                    
            if final_permissions[i]['app_role_assignments']:
                for x in final_permissions[i]['app_role_assignments']:
                    print('\n\tApp Role Assignment:')
                    print('\tPermission Name: ' + x['Permission Name'])
                    print('\tPrincipalDisplayName: ' + x['principalDisplayName'])
                    print('\tResourceDisplayName: ' + x['resourceDisplayName'])
                    print('\tResourceId: ' + x['resourceId'])
            if final_permissions[i]['pim_eligible_roles']:
                for x in final_permissions[i]['pim_eligible_roles']:
                    print('\n\tPIM Eligible Role Assignment:')
                    print('\tRole: ' + x['Role'])
                    print('\tAssignmenttype: ' + x['Assignmenttype'])
                    print('\tAssigned to: ' + x['Name'])
        elif ('group-membership' in i) and not ('owned-apps-group-membership' in i):
            if (final_permissions[i]['azuread_roles']) or (final_permissions[i]['azurerm_roles']) or (final_permissions[i]['classic_admins']) or (final_permissions[i]['app_role_assignments']) or (final_permissions[i]['pim_eligible_roles']):
                out=i.rsplit('/',1)
                print('\nPrivileges of the group ' + out[1] + ' that the principal is a member of:')
                if final_permissions[i]['azuread_roles']:
                    for x in final_permissions[i]['azuread_roles']:
                        print('\n\tAzureAD Role Assignment:')
                        print('\tRole: ' + x['Role'])
                if final_permissions[i]['azurerm_roles']:
                    for x in final_permissions[i]['azurerm_roles']:
                        print('\n\tAzureRM Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tScope: ' + x['Scope'])
                        print('\tPrincipal: ' + x['Principal'])                    
                if final_permissions[i]['classic_admins']:
                    for x in final_permissions[i]['classic_admins']:
                        print('\n\tClassic Administrator Role Assignment:')
                        print('\tRole: ' + x['role'])
                        print('\tEmailAddress: ' + x['emailAddress'])                    
                if final_permissions[i]['app_role_assignments']:
                    for x in final_permissions[i]['app_role_assignments']:
                        print('\n\tApp Role Assignment:')
                        print('\tPermission Name: ' + x['Permission Name'])
                        print('\tPrincipalDisplayName: ' + x['principalDisplayName'])
                        print('\tResourceDisplayName: ' + x['resourceDisplayName'])
                        print('\tResourceId: ' + x['resourceId'])
                if final_permissions[i]['pim_eligible_roles']:
                    for x in final_permissions[i]['pim_eligible_roles']:
                        print('\n\tPIM Eligible Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tAssignmenttype: ' + x['Assignmenttype'])
                        print('\tAssigned to: ' + x['Name'])
        elif ('group-ownership' in i) and not ('owned-apps-group-ownership' in i):
            if (final_permissions[i]['azuread_roles']) or (final_permissions[i]['azurerm_roles']) or (final_permissions[i]['classic_admins']) or (final_permissions[i]['app_role_assignments']) or (final_permissions[i]['pim_eligible_roles']):
                out=i.rsplit('/',1)
                print('\nPrivileges of the group ' + out[1] + ' that the principal is a owner of:')
                if final_permissions[i]['azuread_roles']:
                    for x in final_permissions[i]['azuread_roles']:
                        print('\n\tAzureAD Role Assignment:')
                        print('\tRole: ' + x['Role'])
                if final_permissions[i]['azurerm_roles']:
                    for x in final_permissions[i]['azurerm_roles']:
                        print('\n\tAzureRM Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tScope: ' + x['Scope'])
                        print('\tPrincipal: ' + x['Principal'])                    
                if final_permissions[i]['classic_admins']:
                    for x in final_permissions[i]['classic_admins']:
                        print('\n\tClassic Administrator Role Assignment:')
                        print('\tRole: ' + x['role'])
                        print('\tEmailAddress: ' + x['emailAddress'])                    
                if final_permissions[i]['app_role_assignments']:
                    for x in final_permissions[i]['app_role_assignments']:
                        print('\n\tApp Role Assignment:')
                        print('\tPermission Name: ' + x['Permission Name'])
                        print('\tPrincipalDisplayName: ' + x['principalDisplayName'])
                        print('\tResourceDisplayName: ' + x['resourceDisplayName'])
                        print('\tResourceId: ' + x['resourceId'])
                if final_permissions[i]['pim_eligible_roles']:
                    for x in final_permissions[i]['pim_eligible_roles']:
                        print('\n\tPIM Eligible Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tAssignmenttype: ' + x['Assignmenttype'])
                        print('\tAssigned to: ' + x['Name'])
        elif 'app-ownership' in i: 
            if (final_permissions[i]['azuread_roles']) or (final_permissions[i]['azurerm_roles']) or (final_permissions[i]['classic_admins']) or (final_permissions[i]['app_role_assignments']) or (final_permissions[i]['pim_eligible_roles']):
                out=i.rsplit('/',1)
                print('\nPrivileges of the service principal ' + out[1] + ' that the principal is a owner of:')
                if final_permissions[i]['azuread_roles']:
                    for x in final_permissions[i]['azuread_roles']:
                        print('\n\tAzureAD Role Assignment:')
                        print('\tRole: ' + x['Role'])
                if final_permissions[i]['azurerm_roles']:
                    for x in final_permissions[i]['azurerm_roles']:
                        print('\n\tAzureRM Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tScope: ' + x['Scope'])
                        print('\tPrincipal: ' + x['Principal'])                    
                if final_permissions[i]['classic_admins']:
                    for x in final_permissions[i]['classic_admins']:
                        print('\n\tClassic Administrator Role Assignment:')
                        print('\tRole: ' + x['role'])
                        print('\tEmailAddress: ' + x['emailAddress'])                    
                if final_permissions[i]['app_role_assignments']:
                    for x in final_permissions[i]['app_role_assignments']:
                        print('\n\tApp Role Assignment:')
                        print('\tPermission Name: ' + x['Permission Name'])
                        print('\tPrincipalDisplayName: ' + x['principalDisplayName'])
                        print('\tResourceDisplayName: ' + x['resourceDisplayName'])
                        print('\tResourceId: ' + x['resourceId'])
                if final_permissions[i]['pim_eligible_roles']:
                    for x in final_permissions[i]['pim_eligible_roles']:
                        print('\n\tPIM Eligible Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tAssignmenttype: ' + x['Assignmenttype'])
                        print('\tAssigned to: ' + x['Name'])
        elif 'owned-apps-group-membership' in i:
            if (final_permissions[i]['azuread_roles']) or (final_permissions[i]['azurerm_roles']) or (final_permissions[i]['classic_admins']) or (final_permissions[i]['app_role_assignments']) or (final_permissions[i]['pim_eligible_roles']): 
                out=i.rsplit('/',1)
                print('\nPrivileges of the group ' + out[1] + ' that a owned service principal of the principal is a member of:')
                if final_permissions[i]['azuread_roles']:
                    for x in final_permissions[i]['azuread_roles']:
                        print('\n\tAzureAD Role Assignment:')
                        print('\tRole: ' + x['Role'])
                if final_permissions[i]['azurerm_roles']:
                    for x in final_permissions[i]['azurerm_roles']:
                        print('\n\tAzureRM Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tScope: ' + x['Scope'])
                        print('\tPrincipal: ' + x['Principal'])                    
                if final_permissions[i]['classic_admins']:
                    for x in final_permissions[i]['classic_admins']:
                        print('\n\tClassic Administrator Role Assignment:')
                        print('\tRole: ' + x['role'])
                        print('\tEmailAddress: ' + x['emailAddress'])                    
                if final_permissions[i]['app_role_assignments']:
                    for x in final_permissions[i]['app_role_assignments']:
                        print('\n\tApp Role Assignment:')
                        print('\tPermission Name: ' + x['Permission Name'])
                        print('\tPrincipalDisplayName: ' + x['principalDisplayName'])
                        print('\tResourceDisplayName: ' + x['resourceDisplayName'])
                        print('\tResourceId: ' + x['resourceId'])
                if final_permissions[i]['pim_eligible_roles']:
                    for x in final_permissions[i]['pim_eligible_roles']:
                        print('\n\tPIM Eligible Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tAssignmenttype: ' + x['Assignmenttype'])
                        print('\tAssigned to: ' + x['Name'])
        elif 'owned-apps-group-ownership' in i:
            if (final_permissions[i]['azuread_roles']) or (final_permissions[i]['azurerm_roles']) or (final_permissions[i]['classic_admins']) or (final_permissions[i]['app_role_assignments']) or (final_permissions[i]['pim_eligible_roles']): 
                out=i.rsplit('/',1)
                print('\nPrivileges of the group ' + out[1] + ' that a owned service principal of the principal is a owner of:')
                if final_permissions[i]['azuread_roles']:
                    for x in final_permissions[i]['azuread_roles']:
                        print('\n\tAzureAD Role Assignment:')
                        print('\tRole: ' + x['Role'])
                if final_permissions[i]['azurerm_roles']:
                    for x in final_permissions[i]['azurerm_roles']:
                        print('\n\tAzureRM Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tScope: ' + x['Scope'])
                        print('\tPrincipal: ' + x['Principal'])                    
                if final_permissions[i]['classic_admins']:
                    for x in final_permissions[i]['classic_admins']:
                        print('\n\tClassic Administrator Role Assignment:')
                        print('\tRole: ' + x['role'])
                        print('\tEmailAddress: ' + x['emailAddress'])                    
                if final_permissions[i]['app_role_assignments']:
                    for x in final_permissions[i]['app_role_assignments']:
                        print('\n\tApp Role Assignment:')
                        print('\tPermission Name: ' + x['Permission Name'])
                        print('\tPrincipalDisplayName: ' + x['principalDisplayName'])
                        print('\tResourceDisplayName: ' + x['resourceDisplayName'])
                        print('\tResourceId: ' + x['resourceId'])
                if final_permissions[i]['pim_eligible_roles']:
                    for x in final_permissions[i]['pim_eligible_roles']:
                        print('\n\tPIM Eligible Role Assignment:')
                        print('\tRole: ' + x['Role'])
                        print('\tAssignmenttype: ' + x['Assignmenttype'])
                        print('\tAssigned to: ' + x['Name'])

async def gettenant(domain):

    async with aiohttp.ClientSession() as session:
        async with session.get('https://login.microsoftonline.com/' + domain + '/v2.0/.well-known/openid-configuration') as resp:
            if resp.status != 200:
                print('ERROR (gettenant):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()
                tenantid = data['token_endpoint']
                tenantid = tenantid.split('https://login.microsoftonline.com/')
                tenantid = tenantid[1].split('/oauth2/') 
                tenantid = tenantid[0]
                print('TenantId: ' + tenantid)
    return tenantid

async def get_azuread_roles(objectId, access_token, type):
    """find AzureAD roles"""

    ids = []
    headers = {'Authorization':'Bearer '+access_token}
    #false or true does not seem to make a difference
    body = {"securityEnabledOnly": 'false' }
   
    if type == 'group':        
        async with aiohttp.ClientSession(headers=headers) as session:
            path = 'https://graph.microsoft.com/v1.0/groups/' + objectId + '/getMemberObjects'
            async with session.post(path, json=body) as resp:                
                if resp.status != 200:
                    print('ERROR (get_azuread_roles1):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        ids.append(i)

    elif type == 'servicePrincipal':
        async with aiohttp.ClientSession(headers=headers) as session:
            path = 'https://graph.microsoft.com/v1.0/servicePrincipals/' + objectId + '/getMemberObjects'
            async with session.post(path, json=body) as resp:
                if resp.status != 200:
                    print('ERROR (get_azuread_roles2):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()          
                    for i in data['value']:
                        ids.append(i)
            
    elif type == 'user':
        async with aiohttp.ClientSession(headers=headers) as session:
            path = 'https://graph.microsoft.com/v1.0/users/' + objectId + '/getMemberObjects'
            async with session.post(path, json=body) as resp:
                if resp.status != 200:
                    print('ERROR (get_azuread_roles3):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()           
                    for i in data['value']:
                        ids.append(i)
    azuread_roles = []
    async with aiohttp.ClientSession(headers=headers) as session:
        #should be transitive so no querying for groups necessary
        path = 'https://graph.microsoft.com/v1.0/directoryObjects/getByIds' 
        # skip this part if none were found
        if len(ids)>0:
            body = {"ids": ids}
            async with session.post(path, json=body) as resp:
                    if resp.status != 200:
                        print('ERROR (get_azuread_roles4):\n')
                        error = await resp.text()
                        print (error)
                    else:
                        data = await resp.json() 
                        for i in data['value']:
                            assignments = {}
                            if i['@odata.type'] == '#microsoft.graph.directoryRole':
                                assignments['Role'] =  i['displayName']
                                assignments['Assignment-Id'] = i['id']
                                azuread_roles.append(assignments)
    return azuread_roles    

async def get_approles(objectId, access_token, type):
    """find app role assignments"""
    app_role_assignments = []
    headers = {'Authorization':'Bearer '+access_token}
    assignments = {}

    async with aiohttp.ClientSession(headers=headers) as session:
        if type == 'group':
            path = 'https://graph.microsoft.com/v1.0/groups/' + objectId + '/appRoleAssignments'
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (get_approles):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        assignments = {}
                        path = 'https://graph.microsoft.com/v1.0/servicePrincipals/' + i['resourceId'] 
                        async with session.get(path) as resp:
                            if resp.status != 200:
                                print('ERROR (get_approles):\n')
                                error = await resp.text()
                                print (error)
                            else:
                                data2 = await resp.json()
                                for x in data2['appRoles']:                     
                                    if x['id'] == i['appRoleId']: 
                                        assignments['Permission Name'] = x['value']
                                assignments['appRoleAssignmentId'] = i['id']
                                assignments['appRoleId'] = i['appRoleId']
                                assignments['principalDisplayName'] = i['principalDisplayName']
                                assignments['resourceDisplayName'] = i['resourceDisplayName']
                                assignments['resourceId'] = i['resourceId']
                                app_role_assignments.append(assignments)
            
            
        elif type == 'user':
            path = 'https://graph.microsoft.com/v1.0/users/' + objectId + '/appRoleAssignments'
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (get_approles):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        assignments = {}
                        path = 'https://graph.microsoft.com/v1.0/servicePrincipals/' + i['resourceId'] 
                        async with session.get(path) as resp:
                            if resp.status != 200:
                                print('ERROR (get_approles):\n')
                                error = await resp.text()
                                print (error)
                            else:
                                data2 = await resp.json()
                                for x in data2['appRoles']:                     
                                    if x['id'] == i['appRoleId']: 
                                        assignments['Permission Name'] = x['value']
                                assignments['appRoleAssignmentId'] = i['id']
                                assignments['appRoleId'] = i['appRoleId']
                                assignments['principalDisplayName'] = i['principalDisplayName']
                                assignments['resourceDisplayName'] = i['resourceDisplayName']
                                assignments['resourceId'] = i['resourceId']
                                app_role_assignments.append(assignments)

        elif type == 'servicePrincipal':
            path = 'https://graph.microsoft.com/v1.0/servicePrincipals/' + objectId + '/appRoleAssignments'
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (get_approles):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        assignments = {}
                        path = 'https://graph.microsoft.com/v1.0/servicePrincipals/' + i['resourceId'] 
                        async with session.get(path) as resp:
                            if resp.status != 200:
                                print('ERROR (get_approles):\n')
                                error = await resp.text()
                                print (error)
                            else:
                                data2 = await resp.json()
                                for x in data2['appRoles']:                     
                                    if x['id'] == i['appRoleId']: 
                                        assignments['Permission Name'] = x['value']
                                assignments['appRoleAssignmentId'] = i['id']
                                assignments['appRoleId'] = i['appRoleId']
                                assignments['principalDisplayName'] = i['principalDisplayName']
                                assignments['resourceDisplayName'] = i['resourceDisplayName']
                                assignments['resourceId'] = i['resourceId']
                                app_role_assignments.append(assignments)
    return app_role_assignments

async def getowner(objectId, access_token, type):
    
    headers = {'Authorization':'Bearer ' + access_token}

    out = {}
    localgroups = []
    localapps = []

    async with aiohttp.ClientSession(headers=headers) as session:
        if type == 'user':
            path = 'https://graph.microsoft.com/v1.0/users/' + objectId +'/ownedObjects'
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (getowner1):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        if i['@odata.type'] == '#microsoft.graph.group':
                            localgroups.append(i['id']) 
                            # print('\nGroup Ownership:')
                            # print('Displayname: ' + i['displayName'])
                            # print('ID: ' + i['id'])    
                        elif i['@odata.type'] == '#microsoft.graph.servicePrincipal': 
                            localapps.append(i['id'])
                            # print('\nApp Ownership:')                    
                            # print('Displayname: ' + i['appDisplayName'])
                            # print('Client-Id: ' + i['appId'])
            
        elif type == 'servicePrincipal':
            path = 'https://graph.microsoft.com/v1.0/servicePrincipals/' + objectId +'/ownedObjects'
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (getowner2):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        if i['@odata.type'] == '#microsoft.graph.group':
                            localgroups.append(i['id']) 
                            # print('\nGroup Ownership:')
                            # print('Displayname: ' + i['displayName'])
                            # print('ID: ' + i['id'])    
                        elif i['@odata.type'] == '#microsoft.graph.servicePrincipal': 
                            localapps.append(i['id'])   
                            # print('\nApp Ownership:')                  
                            # print('Displayname: ' + i['appDisplayName'])
                            # print('Client-Id: ' + i['appId'])
        
    out['group owns'] = localgroups
    out['app owns'] = localapps
    return out

async def getpim(object_id,refresh_token,tenantid,graph_token):        
    
    assignments = {}
    pim_eligible_roles = []
    global pimtoken
    
    #AAD Roles
    if not pimtoken:
        #https://api.azrbac.mspim.azure.com/.default works for AAD too
        # id was found by testing / appears to be MS-PIM client-id / could be unique for every tenant
        # Get MS-PIM ID:    
        headers = {'Authorization':'Bearer ' + graph_token}
        path = 'https://graph.microsoft.com/v1.0/servicePrincipals'
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (getpim):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        if i['appDisplayName'] == 'MS-PIM':
                            scope = i['appId']
                            body = {'scope':scope + '/.default','client_id':'1950a258-227b-4e31-a9cf-717495945fc2','grant_type':'refresh_token','refresh_token':refresh_token}
                            async with aiohttp.ClientSession() as session:
                                path = 'https://login.microsoftonline.com/' + tenantid + '/oauth2/v2.0/token'
                                async with session.post(path,data=body) as resp:
                                    if resp.status != 200:
                                        print('ERROR (getpim):\n')
                                        error = await resp.text()
                                        print (error)
                                    else:
                                        out = await resp.json()
                                        pimtoken = out['access_token'] 
    
    headers = {'Authorization':'Bearer ' + pimtoken}    
    async with aiohttp.ClientSession(headers=headers) as session:  
        # AzureRM Roles
        # First get resources that are onboarded to AzureRM
        resources = []            
        path = 'https://api.azrbac.mspim.azure.com/api/v2/privilegedAccess/azureResources/resources'
        async with session.get(path) as resp:
            if resp.status != 200:
                print('ERROR (getpim):\n')
                error = await resp.text()
                print (error)
            else:
                data = await resp.json()              
                for i in data['value']:
                    resources.append(i['id'])                        
        # Query on every ressource that is onboarded to PIM
        # create url list
        resource_urls = []          
        for i in resources:
            resource_urls.append("https://api.azrbac.mspim.azure.com/api/v2/privilegedAccess/azureResources/roleAssignments?$filter=(roleDefinition/resource/id eq '" + i + "') and (assignmentState eq 'Eligible')&$expand=subject,roleDefinition" )

           
        tasks = []
        for i in resource_urls:
            tasks.append(asyncio.ensure_future(url_helper_get(session , i)))
        out = await asyncio.gather(*tasks)

        for response in out:
            for y in response['value']:
                assignments = {}                
                if y['subjectId'] == object_id: 
                    assignments['id'] = y['id']
                    #for users the "principalName" key is better as it includes the full name/ for Groups it is however empty
                    assignments['Name'] = y['subject']['displayName']
                    assignments['Type'] = y['subject']['type']
                    assignments['Assignmenttype'] = 'AzureRM'
                    assignments['Role'] = y['roleDefinition']['displayName']  
                    pim_eligible_roles.append(assignments)

        #AzureAd
        path = 'https://api.azrbac.mspim.azure.com/api/v2/privilegedAccess/aadroles/resources/' + tenantid + "/roleassignments?$expand=subject,roleDefinition&$filter=assignmentState+eq+'Eligible'"
        async with session.get(path) as resp:
                if resp.status != 200:
                    print('ERROR (getpim):\n')
                    error = await resp.text()
                    print (error)
                else:
                    data = await resp.json()
                    for i in data['value']:
                        assignments = {} 
                        if i['subjectId'] == object_id:                        
                            #for users the "principalName" key is better as it includes the full name/ for Groups it is however empty
                            assignments['id'] = i['id']
                            assignments['Name'] = i['subject']['displayName']
                            assignments['Type'] = i['subject']['type']
                            assignments['Assignmenttype'] = 'AzureAD'
                            assignments['Role'] = i['roleDefinition']['displayName']                        
                            pim_eligible_roles.append(assignments)
                        
    # get unique values in each list
    pim_eligible_roles = list({x["id"]: x for x in pim_eligible_roles}.values())        
    
    return pim_eligible_roles
       
async def get_id_specific_priv(object_id,arm_token,graph_token,type,tenantid,cause,refresh_token,roleassignments):  
    """Wrapperfunction to enumerate the specific direct permissions of a principal-id"""           
   
    azuread_roles = []
    azurerm_roles = []
    classic_admins = []
    app_role_assignments = []
    pim_eligible_roles = []

    permissions = {}

    if cause == 'direct':
        if type == 'user':        
            azuread_roles = await get_azuread_roles(object_id ,graph_token, 'user') 
            azurerm_roles = await get_azurerm_roles(roleassignments,object_id,roledefinitions,graph_token)   
            app_role_assignments = await get_approles(object_id ,graph_token, 'user')
            pim_eligible_roles = await getpim(object_id,refresh_token,tenantid,graph_token)
            classic_admins = await get_classic_admins(arm_token, object_id, graph_token)                 
        
        elif type == 'servicePrincipal': 
            azuread_roles = await get_azuread_roles(object_id ,graph_token, 'servicePrincipal') 
            azurerm_roles = await get_azurerm_roles(roleassignments,object_id,roledefinitions,graph_token)  
            app_role_assignments = await get_approles(object_id ,graph_token, 'servicePrincipal') 
    
        elif type == 'group': 
            azuread_roles = await get_azuread_roles(object_id ,graph_token, 'group') 
            azurerm_roles = await get_azurerm_roles(roleassignments,object_id,roledefinitions,graph_token) 
            app_role_assignments = await get_approles(object_id ,graph_token, 'group')
            pim_eligible_roles = await getpim(object_id,refresh_token,tenantid,graph_token)
        
        # Combine into one JSON
        permissions['azuread_roles'] = azuread_roles
        permissions['azurerm_roles'] = azurerm_roles
        permissions['classic_admins'] = classic_admins
        permissions['app_role_assignments'] = app_role_assignments
        permissions['pim_eligible_roles'] = pim_eligible_roles
        # add whole dict to final output, referenced by the cause
        final_permissions['direct'] = permissions
    else:
        if type == 'user':        
            azuread_roles = await get_azuread_roles(object_id ,graph_token, 'user') 
            azurerm_roles = await get_azurerm_roles(roleassignments,object_id,roledefinitions,graph_token)   
            app_role_assignments = await get_approles(object_id ,graph_token, 'user')
            pim_eligible_roles = await getpim(object_id,refresh_token,tenantid,graph_token)
            classic_admins = await get_classic_admins(arm_token, object_id, graph_token)                 
        
        elif type == 'servicePrincipal': 
            azuread_roles = await get_azuread_roles(object_id ,graph_token, 'servicePrincipal') 
            azurerm_roles = await get_azurerm_roles(roleassignments,object_id,roledefinitions,graph_token)  
            app_role_assignments = await get_approles(object_id ,graph_token, 'servicePrincipal')        
                
        elif type == 'group': 
            azuread_roles = await get_azuread_roles(object_id ,graph_token, 'group') 
            azurerm_roles = await get_azurerm_roles(roleassignments,object_id,roledefinitions,graph_token) 
            app_role_assignments = await get_approles(object_id ,graph_token, 'group')
            pim_eligible_roles = await getpim(object_id,refresh_token,tenantid,graph_token)
        
        # Combine into one JSON
        permissions['azuread_roles'] = azuread_roles
        permissions['azurerm_roles'] = azurerm_roles
        permissions['classic_admins'] = classic_admins
        permissions['app_role_assignments'] = app_role_assignments
        permissions['pim_eligible_roles'] = pim_eligible_roles
        # add whole dict to final output, referenced by the cause
        final_permissions[cause + '/' + object_id] = permissions

async def get_indirect(object_id, graph_token, type):
    """get group owns / app owns / group memberships"""

    # is transitive, therefor running it once will include all memberships
    await get_group_memberships(object_id ,graph_token, type) 

    if type == 'user':   
        ownerships = await getowner(object_id, graph_token, type)
        group_ownership=ownerships['group owns']
        app_ownership=ownerships['app owns']
        for i in group_ownership:
            group_owns.append(i)
        for i in app_ownership:
            apps.append(i)        

    elif type == 'servicePrincipal': 
        ownerships = await getowner(object_id, graph_token, type)
        group_ownership=ownerships['group owns']
        for i in group_ownership:
            group_owns.append(i)

async def main():
    if args.clear_all:
        clearall()
        sys.exit(0)
    elif args.clear_token:
        cleartoken()
        sys.exit(0)

    if args.tenant_id:
        tenantid=args.tenant_id
    elif args.domain:        
        tenantid= await gettenant(args.domain)
    else:
        print('pls provide a domain or tenant-id')   
    
    if args.refresh_token:
        refresh_token=args.refresh_token
        token = await refreshtoken('https://graph.microsoft.com/.default',refresh_token,tenantid)
        graph_token = token['access_token'] 
        token = await refreshtoken('https://management.azure.com/.default',refresh_token,tenantid)
        arm_token = token['access_token'] 
    else:
        out = devicecodeflow(tenantid) 
        refresh_token=out['refresh_token']         
        token = await refreshtoken('https://management.azure.com/.default',refresh_token,tenantid)
        arm_token =  token['access_token']  
        token = await refreshtoken('https://graph.microsoft.com/.default',refresh_token,tenantid)
        graph_token = token['access_token'] 

    if args.user_principal:
       object_id = await getidbyname(args.user_principal,graph_token)
    else:
        # if user or group it will only print output however if client-id was provided it will get the Object id
        object_id = await getnamebyid(args.object_id,graph_token)

    await get_subscriptions(arm_token)

    # global roleassignments
    # if os.path.exists('roleassignments.json'):
    #     file = open('roleassignments.json', 'r')
    #     roleassignments = json.load(file)
    # else:
    await get_resources(arm_token)

    type = await gettype(object_id , graph_token)

    global groups
    global group_owns

    tasks = []          
    if type == 'user': 
        tasks.append(get_id_specific_priv(object_id,arm_token,graph_token,'user',tenantid,'direct',refresh_token,roleassignments))
        tasks.append(get_indirect(object_id, graph_token, type))
        await asyncio.gather(*tasks)        
        # users can be group members or owners therefor check their privileges
        if len(groups)>0:
            tasks = [] 
            for i in groups:                
                tasks.append(get_id_specific_priv(i,arm_token,graph_token,'group',tenantid,'group-membership',refresh_token,roleassignments))              
        if len(group_owns)>0:
            for i in group_owns:
                tasks.append(get_id_specific_priv(i,arm_token,graph_token,'group',tenantid,'group-ownership',refresh_token,roleassignments)) 
        if tasks:
            await asyncio.gather(*tasks)               
        # users can also own apps therefor repeat below segment about service principals
        # clear lists because privileges for groups were already queried
        groups = []
        group_owns = []
        if len(apps)>0:
            tasks = [] 
            for i in apps:                
                tasks.append(get_id_specific_priv(i,arm_token,graph_token,'servicePrincipal',tenantid,'app-ownership',refresh_token,roleassignments))
                tasks.append(get_indirect(i, graph_token, 'servicePrincipal'))
                await asyncio.gather(*tasks)
                # service principals can only be group members or owners therefor check their privileges
                tasks = [] 
                if len(groups)>0:
                    for x in groups:
                        tasks.append(get_id_specific_priv(x,arm_token,graph_token,'group',tenantid,'owned-apps-group-membership',refresh_token,roleassignments))
                if len(group_owns)>0:
                    for x in group_owns:
                        tasks.append(get_id_specific_priv(x,arm_token,graph_token,'group',tenantid,'owned-apps-group-ownership',refresh_token,roleassignments))                        
                if tasks:
                    await asyncio.gather(*tasks)  

    elif type == 'servicePrincipal': 
        tasks.append(get_id_specific_priv(object_id,arm_token,graph_token,'servicePrincipal',tenantid,'direct',refresh_token,roleassignments))
        tasks.append(get_indirect(object_id, graph_token, type))
        await asyncio.gather(*tasks)
        # service principals can only be group members or owners therefor check their relevant privileges
        tasks = [] 
        if len(groups)>0:
            for i in groups:
                tasks.append(get_id_specific_priv(i,arm_token,graph_token,'group',tenantid,'group-membership',refresh_token,roleassignments))                
        if len(group_owns)>0:
            for i in group_owns:
                tasks.append(get_id_specific_priv(i,arm_token,graph_token,'group',tenantid,'group-ownership',refresh_token,roleassignments))
        if tasks:
            await asyncio.gather(*tasks)                  
                
     
    elif type == 'group': 
        tasks.append(get_id_specific_priv(object_id,arm_token,graph_token,'group',tenantid,'direct',refresh_token,roleassignments))
        tasks.append(get_indirect(object_id, graph_token, type))      
        await asyncio.gather(*tasks)   
        # groups can only be group members therefor check their privileges
        tasks = [] 
        if len(groups)>0: 
            # in the get_group_memberships function the queried group itself was added to the groups list. Has to be removed.  
            groups.remove(object_id)
            for i in groups:
                tasks.append(get_id_specific_priv(i,arm_token,graph_token,'group',tenantid,'group-membership',refresh_token,roleassignments))
        if tasks:
            await asyncio.gather(*tasks)       

    if args.path:
        file = open(args.path, "w")  
        json.dump(final_permissions, file)  
        file.close() 
    else:
        await output(final_permissions)  
    
if __name__=='__main__':

    parser = argparse.ArgumentParser( description = '-')
    parser.add_argument('-t', '--tenant-id')
    parser.add_argument('-d', '--domain')
    parser.add_argument('-r', '--refresh-token')
    parser.add_argument('-i', '--object-id')
    # searching by name works for users only
    parser.add_argument('-u', '--user-principal')
    parser.add_argument('-c', '--clear-all',  action='store_true')  
    parser.add_argument('-ct', '--clear-token',  action='store_true') 
    parser.add_argument('-o','--path')     
    args = parser.parse_args()

    #needed on windows:
    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())

    