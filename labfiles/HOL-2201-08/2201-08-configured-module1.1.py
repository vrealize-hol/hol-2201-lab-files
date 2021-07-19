import urllib3
import sys
import subprocess
import time
from time import sleep
import requests
import json
urllib3.disable_warnings()

debug = True

vra_fqdn = 'vr-automation.corp.local'
vrops_fqdn = 'vr-operations.corp.local'
vrslcm_fqdn = 'vr-lcm.corp.local'

def log(msg):
    if debug:
        sys.stdout.write(msg + '\n')
    file = open("C:\\hol\\vraConfig.log", "a")
    file.write(msg + '\n')
    file.close()

###################
## vRSLCM Functions
###################

def addAdGroup():
    api_url = '{0}idp/dirConfigs/syncprofile'.format(api_url_base)
    data = {
        "directoryConfigId":"70665188-ddb3-49f6-98f7-327e69572de5",
        "syncProfileGroup": 
        {
            "excludeNestedGroupMembers":"false",
            "identityGroupInfo":
            {
                "OU=Groups,OU=HOL,DC=corp,DC=local":
                {
                    "mappedGroupData":
                    [
                        {
                            "mappedGroup":
                            {
                                "horizonName":"app-support-team@corp.local",
                                "dn":"CN=app-support-team,OU=Groups,OU=HOL,DC=corp,DC=local",
                                "objectGuid":"8d09eee9-4cd7-4d16-989b-d756000b7a22",
                                "groupBaseDN":"OU=Groups,OU=HOL,DC=corp,DC=local",
                                "source":"DIRECTORY"
                            },
                            "selected":"true"
                        },
                        {
                            "mappedGroup":
                            {
                                "horizonName":"web-admin-team@corp.local",
                                "dn":"CN=web-admin-team,OU=Groups,OU=HOL,DC=corp,DC=local",
                                "objectGuid":"4365c789-2979-428b-a3d0-b7960d01d800",
                                "groupBaseDN":"OU=Groups,OU=HOL,DC=corp,DC=local",
                                "source":"DIRECTORY"
                            },
                            "selected":"true"
                        },
                        {
                            "mappedGroup":
                            {
                                "horizonName":"web-dev-team@corp.local",
                                "dn":"CN=web-dev-team,OU=Groups,OU=HOL,DC=corp,DC=local",
                                "objectGuid":"9f9df8cb-9ed0-4cb6-a971-341331bdf8ef",
                                "groupBaseDN":"OU=Groups,OU=HOL,DC=corp,DC=local",
                                "source":"DIRECTORY"
                            },
                            "selected":"true"
                        }
                    ],
                    "selected":"false",
                    "numSelected":3,
                    "numTotal":4
                    }
                }
            },
            "triggerDryrun":"false",
            "vidmDomainName":"corp.local",
            "baseTenantHostname":"rainpole-portal.corp.local",
            "vidmAdminPassword":"locker:password:3c18cac5-fa10-4c96-916b-870d28019817:VMware1!",
            "vidmHost":"rainpole-portal.corp.local",
            "vidmAdminUser":"admin",
            "vidmVersion":"3.3.5",
            "vidmRootPassword":"locker:password:3c18cac5-fa10-4c96-916b-870d28019817:VMware1!",
            "vidmSshPassword":"locker:password:3c18cac5-fa10-4c96-916b-870d28019817:VMware1!",
            "vidmOAuthServiceClientId":"Service__OAuth2Client",
            "vidmOAuthServiceClientSecret":"jurOkijbaxqlB5VpLtuEY920sYkHdMjX",
            "tenancyEnabled":"true",
            "vidmProductCertificate":"locker:certificate:d8845355-dd9a-42f4-9825-a597543e59b9:identity-manager",
            "clusteredVidm":"false"
        }
    response = requests.post(api_url, headers=headers,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('Successfully added AD group to vRSLCM')
    else:
        log('Failed to add AD group to vRSLCM. Exiting ...')
        quit()


def syncAdGroup():
    api_url = '{0}idp/dirConfigs/syncprofile/sync'.format(api_url_base)
    data = {
        "directoryConfigId": "70665188-ddb3-49f6-98f7-327e69572de5",
        "vidmDomainName": "corp.local",
        "baseTenantHostname": "rainpole-portal.corp.local",
        "vidmAdminPassword": "locker:password:3c18cac5-fa10-4c96-916b-870d28019817:VMware1!",
        "vidmHost": "rainpole-portal.corp.local",
        "vidmAdminUser": "admin",
        "vidmVersion": "3.3.5",
        "vidmRootPassword": "locker:password:3c18cac5-fa10-4c96-916b-870d28019817:VMware1!",
        "vidmSshPassword": "locker:password:3c18cac5-fa10-4c96-916b-870d28019817:VMware1!",
        "vidmOAuthServiceClientId": "Service__OAuth2Client",
        "vidmOAuthServiceClientSecret": "jurOkijbaxqlB5VpLtuEY920sYkHdMjX",
        "tenancyEnabled": "true",
        "vidmProductCertificate": "locker:certificate:d8845355-dd9a-42f4-9825-a597543e59b9:identity-manager",
        "clusteredVidm": "false"
        }
    response = requests.post(api_url, headers=headers,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('Successfully synced AD group in vRSLCM')
    else:
        log('Failed to sync AD group in vRSLCM. Exiting ...')
        quit()



###################
## vRA Functions
###################

def getVraToken(user_name, pass_word):
    api_url = '{0}csp/gateway/am/api/login?access_token'.format(api_url_base)
    data = {
        "username": user_name,
        "password": pass_word
    }
    response = requests.post(api_url, headers=headers,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = response.json()
        refreshToken = json_data['refresh_token']
        log('Successfully got API access token from vRA')
    else:
        log('Failed to get API access token from vRA. Exiting ...')
        quit()

    api_url = '{0}iaas/api/login'.format(api_url_base)
    data = {
        "refreshToken": refreshToken
    }
    response = requests.post(api_url, headers=headers,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = response.json()
        bearerToken = json_data['token']
        log('Successfully got API bearer token from vRA')
        return(bearerToken)
    else:
        log('Failed to get API bearer token from vRA. Exiting ...')
        quit()


def checkEnterpriseGroups(groupName):
    api_url = '{0}csp/gateway/portal/api/orgs/7e3973a7-94dc-4953-8581-f1e912768f34/groups'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        results = response.json()['results']
        found = False
        for result in results:
            if groupName in result['displayName']:
                found = True
        return(found)

def getAvailableEnterpriseGroups(searchString):
    api_url = '{0}csp/gateway/am/api/groups/search?searchTerm={1}'.format(api_url_base, searchString)
    groupFound = False
    attempts = 0
    while not groupFound:
        attempts += 1
        response = requests.get(api_url, headers=headers1, verify=False)
        if response.status_code == 200:
            content = response.json()
            resultCount = content['totalResults']
            if resultCount == 1:
                groupFound = True
                groupId = content['results'][0]['id']
            else:
                if attempts > 24:     # 60 seconds
                    log('Failed to find AD group in vRA. Exiting ...')
                    quit()
                else:
                    log(' Waiting for AD group to be seen in vRA')
                    time.sleep(5)       # wait 5 seconds and try again
    return(groupId)


def setGroupRoles(group):
    api_url = '{0}csp/gateway/portal/api/orgs/7e3973a7-94dc-4953-8581-f1e912768f34/groups'.format(api_url_base)
    data = {
        "ids":[group],
        "organizationRoleNames":["org_member"],
        "serviceRoles":[
            {
                "serviceDefinitionId":"7564d7c7-db7f-4738-8ec8-d6fa26a8d28c",
                "serviceRoleNames":["catalog:user"]
            },
            {
                "serviceDefinitionId":"f2bc3347-90dd-41b0-810f-22b78e59511b",
                "serviceRoleNames":["CodeStream:viewer"]
            }
            ]
        }
    response = requests.post(api_url, headers=headers1, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        content = response.json()
        log('Added enterprise group roles')
    else:
        log('Was not able to set enterprise group roles. Exiting ...')
        quit()

def createProject():
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    data = {
        "name": "Web Development",
                "zoneAssignmentConfigurations": [
                    {
                        "zoneId": "0acaaec6-cf2d-4610-baaf-25890f06d3c9",
                        "maxNumberInstances": 10,
                        "priority": 0,
                        "cpuLimit": 20,
                        "memoryLimitMB": 10240,
                        "storageLimitGB": 200
                    }
                ],
        "administrators": [
                    {
                        "type": "user",
                        "email": "devmgr@corp.local"
                    }
                ],
        "members": [
                    {
                        "type": "group",
                        "email": "web-dev-team@corp.local@corp.local"
                    }
                ],
        "machineNamingTemplate": "${resource.name}${####}",
        "sharedResources": "false"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = response.json()
        project_id = json_data['id']
        log('Successfully created the Project')
        return project_id
    else:
        log('Failed to create the Project. Exiting ...')
        quit()

def configureGithub(projectId):
    # adds GitHub blueprint integration with the Web Dev Project
    api_url = '{0}content/api/sources'.format(api_url_base)
    data = {
        "typeId":"com.gitlab",
        "config":{
            "integrationId":"a8b6084f-81b1-4ad2-a5af-135e0428445c",
            "repository":"hol/stc-web-development",
            "path":"cloud-templates",
            "branch":"main",
            "contentType":"blueprint"
        },
        "projectId": projectId,
        "name":"GitLab CS",
        "syncEnabled": "true"
        }
    projectFound = False
    attempts = 0
    while not projectFound:
        response = requests.post(api_url, headers=headers1,
                                data=json.dumps(data), verify=False)
        if response.status_code == 201:
            log('Successfully added cloud template repo to project')
            projectFound = True
        else:
            attempts += 1
            if attempts > 12:    # 60 seconds and still no integration
                log('Failed to add the cloud template repo to project. Exiting ...')
                quit()
            else:
                log('  Waiting for GitLab integration with the project')
                time.sleep(5)

def updateABX():
    # updates the ABX action to apply to all projects
    actionId = '8a74802079c6f2870179c75b69f00000'
    initialProjectId = 'c5540053-d251-480d-8a5e-7d9579b45c05'
    api_url = '{0}abx/api/resources/actions/{1}'.format(api_url_base, actionId)
    data = {
        "name":"Rename Cloud Machine",
        "metadata":{
            
        },
        "runtime":"python",
        "source":"def handler(context, inputs):\r\n    \"\"\"Set a name for a machine\r\n\r\n    :param inputs\r\n    :param inputs.resourceNames: Contains the original name of the machine.\r\n           It is supplied from the event data during actual provisioning\r\n           or from user input for testing purposes.\r\n    :param inputs.newName: The new machine name to be set.\r\n    :return The desired machine name.\r\n    \"\"\"\r\n    old_name = inputs[\"resourceNames\"][0]\r\n    new_name = inputs[\"customProperties\"][\"machineName\"]\r\n\r\n    outputs = {}\r\n    outputs[\"resourceNames\"] = inputs[\"resourceNames\"]\r\n    outputs[\"resourceNames\"][0] = new_name\r\n\r\n    print(\"Setting machine name from {0} to {1}\".format(old_name, new_name))\r\n\r\n    return outputs\r\n",
        "entrypoint":"handler",
        "inputs":{
            
        },
        "cpuShares":1024,
        "memoryInMB":300,
        "timeoutSeconds":600,
        "deploymentTimeoutSeconds":900,
        "actionType":"SCRIPT",
        "provider":"on-prem",
        "configuration":{
            "const_azure-system_managed_identity":"false"
        },
        "system":"false",
        "shared":"true",
        "asyncDeployed":"false",
        "projectId":"c5540053-d251-480d-8a5e-7d9579b45c05",
        "orgId":"7e3973a7-94dc-4953-8581-f1e912768f34",
        "id":"8a74802079c6f2870179c75b69f00000",
        "selfLink":"/abx/api/resources/actions/8a74802079c6f2870179c75b69f00000?projectId=c5540053-d251-480d-8a5e-7d9579b45c05",
        "scriptSource":0
        }
    response = requests.put(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('Successfully set extensibilty action to shared')
    else:
        log('Failed to set extensibility action to shared. Exiting ...')
        quit()

def updateSubscription(projectId):
    # Updates the event broker subscription to include the web dev project
    api_url = '{0}event-broker/api/subscriptions'.format(api_url_base)
    data = {
        "id":"sub_1622814224983",
        "type":"RUNNABLE",
        "name":"Rename Cloud Machine",
        "description":"",
        "disabled":"false",
        "eventTopicId":"compute.allocation.pre",
        "subscriberId":"abx-jbNQ6gIBff5ojEBi",
        "blocking":"true",
        "contextual":"false",
        "criteria":"event.data.customProperties[\"machineName\"] != undefined",
        "runnableType":"extensibility.abx",
        "runnableId":"8a74802079c6f2870179c75b69f00000",
        "timeout":0,
        "priority":10,
        "recoverRunnableType":"null",
        "recoverRunnableId":"null",
        "constraints":{
            "projectId":[
                "c5540053-d251-480d-8a5e-7d9579b45c05",
                projectId
            ]
        }
        }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('Successfully added the web dev project to the Action subscription')
    else:
        log('Failed to add the web dev project to the Action subscription. Exiting ...')
        quit()

def getCloudTemplateId(projectID, ctName):
    api_url = '{0}blueprint/api/blueprints'.format(api_url_base)
    templateFound = False
    attempts = 0
    while not templateFound:
        response = requests.get(api_url, headers=headers1, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            templates = json_data['content']
            for template in templates:
                if ctName in template['name']:  # Looking to match the cloud template name
                    if projectID in template['projectId']:
                        ctId = template['id']
                        log('Found the {0} cloud template'.format(ctName))
                        return ctId
            attempts += 1
            if attempts > 6:    # still waiting after 30 seconds
                log('Failed to find the cloud template named ' + ctName + '. Exiting ...')
                quit()
            else:
                log('  Waiting for cloud templates to sync from the GitLab repo')
                time.sleep(5)
        else:
            log('Failed to find the cloud template for this project. Exiting ...')
            quit()


def releaseCloudTemplate(bpid, ver):
    api_url = '{0}blueprint/api/blueprints/{1}/versions/{2}/actions/release'.format(
        api_url_base, bpid, ver)
    data = {}
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('Successfully released the cloud template to the catalog')
    else:
        log('Failed to release the cloud template to the catalog. Exiting ...')
        quit()

def addContentSoure(projid):
    # adds cloud templates from 'projid' project as a content source
    api_url = '{0}catalog/api/admin/sources'.format(api_url_base)
    data = {
        "name": "Web Development Templates",
        "typeId": "com.vmw.blueprint",
        "description": "Released cloud templates in the Web Development project",
        "config": {"sourceProjectId": projid},
        "projectId": projid
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = response.json()
        sourceId = json_data["id"]
        log('Successfully added Web Dev cloud templates as a catalog source')
        return sourceId
    else:
        log('Failed to add Web Dev cloud templates as a catalog source. Exiting ...')
        quit()


def shareCTs(source, project):
    # shares cloud templates content (source) from 'projid' project to the catalog
    api_url = '{0}catalog/api/admin/entitlements'.format(api_url_base)
    data = {
        "definition": {"type": "CatalogSourceIdentifier", "id": source},
        "projectId": project
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('Successfully added cloud template catalog entitlement')
    else:
        log('Failed to add cloud template catalog entitlement. Exiting ...')
        quit()

def getContentId():
    # returns the item ID of the Web Dev Base Linux cloud template content
    api_url = '{0}catalog/api/admin/items'.format(api_url_base)
    contentFound = False
    attempts = 0
    while not contentFound:
        response = requests.get(api_url, headers=headers1, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            items = json_data['content']
            for item in items:
                if item['sourceName'] == 'Web Development Templates':
                    if item['name'] == 'Base Linux Server':
                        Id = item['id']
                        log('Got content item ID')
                        return Id
            attempts += 1
            if attempts > 6:    # 30 seconds
                log('Failed to add web-dev templates as Service Broker content')
                quit()
            else:
                log('  Waiting for web-dev templates to be available to Service Broker')
                time.sleep(5)


def updateIcon(itemId):
    # applies the custom icon to the catalog item
    api_url = '{0}catalog/api/admin/items/{1}'.format(api_url_base, itemId)
    data = {
        "iconId":"85bf95a3-5a28-3de6-bcd6-26dc305184b8",
        "bulkRequestLimit":1
        }
    response = requests.patch(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('Successfully updated the content item icon')
    else:
        log('Failed to update the content item icon. Exiting ...')
        quit()


def updateForm(itemId):
    # adds the custom form for the catalog item
    api_url = '{0}form-service/api/forms'.format(api_url_base)
    data = {
        "name":"Base Linux Server",
        "form":"{\"layout\":{\"pages\":[{\"id\":\"page_general\",\"sections\":[{\"id\":\"section_project\",\"fields\":[{\"id\":\"project\",\"display\":\"dropDown\",\"signpostPosition\":\"right-middle\"}]},{\"id\":\"section_deploymentName\",\"fields\":[{\"id\":\"deploymentName\",\"display\":\"textField\",\"signpostPosition\":\"right-middle\",\"state\":{\"visible\":true,\"read-only\":false}}]},{\"id\":\"section_image\",\"fields\":[{\"id\":\"image\",\"display\":\"dropDown\",\"state\":{\"visible\":true,\"read-only\":false},\"signpostPosition\":\"right-middle\"}]},{\"id\":\"section_flavor\",\"fields\":[{\"id\":\"flavor\",\"display\":\"dropDown\",\"state\":{\"visible\":true,\"read-only\":false},\"signpostPosition\":\"right-middle\"}]},{\"id\":\"section_machineName\",\"fields\":[{\"id\":\"machineName\",\"display\":\"textField\",\"state\":{\"visible\":true,\"read-only\":false},\"signpostPosition\":\"right-middle\"}]},{\"id\":\"section_projectCode\",\"fields\":[{\"id\":\"projectCode\",\"display\":\"dropDown\",\"state\":{\"visible\":true,\"read-only\":false},\"signpostPosition\":\"right-middle\"}]}],\"title\":\"General\",\"state\":{}}]},\"schema\":{\"project\":{\"label\":\"Project\",\"type\":{\"dataType\":\"string\",\"isMultiple\":false},\"valueList\":{\"id\":\"projects\",\"type\":\"scriptAction\"},\"constraints\":{\"required\":true}},\"deploymentName\":{\"label\":\"Deployment Name\",\"type\":{\"dataType\":\"string\",\"isMultiple\":false},\"constraints\":{\"required\":true,\"max-value\":80}},\"image\":{\"label\":\"Operating System\",\"type\":{\"dataType\":\"string\",\"isMultiple\":false},\"valueList\":[{\"label\":\"Ubuntu20\",\"value\":\"Ubuntu20\"},{\"label\":\"Ubuntu18\",\"value\":\"Ubuntu18\"}],\"constraints\":{\"required\":true}},\"flavor\":{\"label\":\"Server size\",\"type\":{\"dataType\":\"string\",\"isMultiple\":false},\"valueList\":[{\"label\":\"small\",\"value\":\"small\"},{\"label\":\"medium\",\"value\":\"medium\"},{\"label\":\"large\",\"value\":\"large\"}],\"constraints\":{\"required\":true}},\"machineName\":{\"label\":\"Server Name\",\"type\":{\"dataType\":\"string\",\"isMultiple\":false},\"constraints\":{\"required\":true}},\"projectCode\":{\"label\":\"Project Code\",\"type\":{\"dataType\":\"string\",\"isMultiple\":false},\"valueList\":{\"id\":\"com.vmware.hol.2201.08/getProjectCodes\",\"type\":\"scriptAction\",\"parameters\":[]},\"constraints\":{\"required\":true}}},\"options\":{\"externalValidations\":[]}}",
        "styles":"null",
        "status":"on",
        "type":"requestForm",
        "sourceId":itemId,
        "sourceType":"com.vmw.blueprint"
        }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('Successfully updated the content item form')
    else:
        log('Failed to update the content item form. Exiting ...')
        quit()


def getCatId(projId):
    api_url = '{0}catalog/api/items'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        catItems = json_data["content"]
        itemName = 'Base Linux Server'
        for catItem in catItems:
            if itemName in catItem["name"]:
                projectIds = catItem['projectIds']
                if projectIds[0] == projId:
                    catalogId = catItem['id']
                    log('Found the catalog item ID')
                    return catalogId
    else:
        log('Failed to get the catalog item ID. Exiting ...')
        quit()


def deployCatItem(catId, project):
    # shares blueprint content (source) from 'projid' project to the catalog
    api_url = '{0}catalog/api/items/{1}/request'.format(api_url_base, catId)
    data = {
        "deploymentName":"STC Demo",
        "reason":"null",
        "projectId":project,
        "bulkRequestCount":1,
        "inputs":{
            "image":"Ubuntu18",
            "flavor":"small",
            "machineName":"web01",
            "projectCode":"A1234"
        }
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('Successfully deployed the catalog item')
    else:
        log('Failed to deploy the catalog item. Exiting ...')
        quit()

###################
## vROps Functions
###################

def getVropsToken(user, passwd):
    api_url = '{0}auth/token/acquire'.format(api_url_base)
    data = {
        "username": user,
        "password": passwd
    }
    response = requests.post(api_url, headers=headers,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = response.json()
        refreshToken = json_data['token']
        log('Retreived vROps API refresh token')
        return refreshToken
    else:
        log('Failed to get vROps API refresh token. Exiting ...')
        quit()


def waitForVM(vmName):
    # check for the VM name in inventory and wait until it's found or the operation times out
    # this funcion not needed but will keep in script for future use
    api_url = '{0}resources?name={1}'.format(api_url_base, vmName)
    attempts = 0
    maxAttempts = 50    # multiply by 10 seconds to set maximum wait time to find the VM
    while attempts < maxAttempts:
        response = requests.get(api_url, headers=headers1, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            resources = json_data['resourceList']
            if len(resources) > 0:
                log('The ' + vmName + ' object was found. Proceeding with configuring vROps.')
                return 1
            else:
                attempts += 1
                time.sleep(10)
    log('Failed to find the ' + vmName + ' object in a timely manner. Exiting ...')
    quit()


def createCustomGroup():
    # creates the vROps custom group
    api_url = '{0}resources/groups'.format(api_url_base)
    data = {
        "resourceKey" : {
            "name" : "Web Development Workloads",
            "adapterKindKey" : "Container",
            "resourceKindKey" : "Cloud Project"
        },
        "autoResolveMembership" : "true",
        "membershipDefinition" : {
            "rules" : [ {
            "resourceKindKey" : {
                "resourceKind" : "VirtualMachine",
                "adapterKind" : "VMWARE"
            },
            "propertyConditionRules" : [ {
                "key" : "summary|tag",
                "stringValue" : "Web Development",
                "compareOperator" : "CONTAINS"
            } ]
            } ]
        }
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = response.json()
        grpId = json_data['id']
        log('Successfully created the custom group')
        return grpId
    else:
        log('Failed to create the custom group. Exiting ...')
        quit()


def assignGroupToPolicy(customGroupId):
    # imports the web-dev AD group and assignes it to the created custom group
    api_url = '{0}policies/apply'.format(api_url_base)
    data = {
        "id" : "5d5abee4-d57b-4844-b1ff-1c31da827a94",
        "groups" : [ customGroupId ]
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('Successfully added the custom group to the HOL policy')
    else:
        log('Failed to add the custom group to the HOL policy. Exiting ...')
        quit()


def importAdGroup(customGroupId):
    # imports the web-dev AD group and assignes it to the created custom group
    api_url = '{0}auth/usergroups'.format(api_url_base)
    data = {
        "authSourceId": "f04a3838-1491-497b-8382-a4d75e5b7096",
        "name": "web-dev-team@corp.local",
        "description": "Web Developers AD Group",
        "displayName": "web-dev-team@corp.local",
        "userIds": [],
        "roleNames": [
            "Cloud Project Users"
        ],
        "role-permissions": [
        {
            "roleName": "Cloud Project Users",
            "traversal-spec-instances": [
                {
                "adapterKind": "?",
                "resourceKind": "?",
                "name": "Custom Groups",
                "resourceSelection": [
                {
                    "type": "PROPAGATE",
                    "resourceId": [
                        customGroupId
                    ]
                }
                ],
                "selectAllResources": "false"
            }
            ],
            "allowAllObjects": "false"
        }
        ]
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('Successfully imported the web-dev AD group')
    else:
        log('Failed to import the web-dev AD group. Exiting ...')
        quit()


##### MAIN SCRIPT #####

##########################################
# CONFIGURE vRSLCM
##########################################
log('*** Configuring vRSLCM')

api_url_base = 'https://' + vrslcm_fqdn + '/lcm/authzn/api/'

headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
            'Authorization': 'Basic YWRtaW5AbG9jYWw6Vk13YXJlMSE='}

addAdGroup()
syncAdGroup()

log('\n*** IMPORTANT ***')
log('You must complete some steps in the vRealize Automation user interface before continuing\n')
log('Once you have performed the steps shown in module 2 of the lab manual,')
log('  you can return here and continue below\n')

"""
###########################################
# CONFIGURE vRA
###########################################
log('*** Configuring vRA')

api_url_base = "https://" + vra_fqdn + "/"
headers = {'Content-Type': 'application/json'}
access_key = getVraToken("holadmin@corp.local", "VMware1!")

headers1 = {'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(access_key)}

# Add AD group to vRA
groupName = 'web-dev'

if checkEnterpriseGroups(groupName):
    logMessage = 'The ' + groupName + ' group already exists in vRA'
    log('\n')
    log(logMessage)
    log('This script cannot proceed. You must complete module 1 --OR--')
    log('   end this lab and start a new lab where you can bypass module 1 by running this script\n')
    log('See the beginning of modlue 2 in the lab manual for instructions.\n\n')
    quit()
else:
    log('Did not find the {0} group in vRA. Adding it.'.format(groupName))

id = getAvailableEnterpriseGroups(groupName)
setGroupRoles(id)

# Add the project to Cloud Assembly
projId = createProject()

# Add the GitHub cloud template repo to the project
configureGithub(projId)

# Update the ABX action
updateABX()

# Update the subscription
updateSubscription(projId)

# Find the cloud template Id and then release the template to the catalog
templateId = getCloudTemplateId(projId, 'Base Linux Server')
releaseCloudTemplate(templateId, 1)

# Add web dev cloud templates as content source in Service Broker
catSource = addContentSoure(projId)
shareCTs(catSource, projId)

# Get the id of the content item and update its icon and form
contentId = getContentId()
updateIcon(contentId)
updateForm(contentId)

# Deploy the catalog item
catId = getCatId(projId)
deployCatItem(catId, projId)


##########################################
# CONFIGURE vROps
##########################################
log('*** Configuring vROps')

api_url_base = 'https://' + vrops_fqdn + '/suite-api/api/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
access_key = getVropsToken('admin', 'VMware1!')

headers1 = {'Content-Type': 'application/json', 'Accept': 'application/json',
            'Authorization': 'vRealizeOpsToken {0}'.format(access_key)}

# Create the custom group and assign it to the policy
CustomGroupId = createCustomGroup()
assignGroupToPolicy(CustomGroupId)

# Import the AD group and assign role and objects
importAdGroup(CustomGroupId)

log('\n\n\nConfiguration script completed')
log('Follow instructions in the lab manual to complete the setup before proceeding.')

"""