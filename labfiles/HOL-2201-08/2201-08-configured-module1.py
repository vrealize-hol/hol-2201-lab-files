import urllib3
import sys
import re
import subprocess
from time import strftime, sleep
import calendar
import datetime
from random import seed, randint
from boto3.dynamodb.conditions import Key, Attr
import boto3
import traceback
import os
import time
import requests
import json
urllib3.disable_warnings()

debug = True

github_key = os.getenv('github_key')
slack_api_key = 'T024JFTN4/B0150SYEHFE/zNcnyZqWvUcEtaqyiRlLj86O'

vra_fqdn = 'vr-automation.corp.local'
vrops_fqdn = 'vr-operations.corp.local'
vrslcm_fqdn = 'vr-lcm.corp.local'

gitlab_api_url_base = "http://gitlab.corp.local/api/v4/"
gitlab_token_suffix = "?private_token=H-WqAJP6whn6KCP2zGSz"
gitlab_header = {'Content-Type': 'application/json'}

# set internet proxy for for communication out of the vPod
proxies = {
    "http": "http://192.168.110.1:3128",
    "https": "https://192.168.110.1:3128"
}

def get_vlp_urn():
    # determine current pod's URN (unique ID) using Main Console guestinfo
    # this uses a VLP-set property named "vlp_vapp_urn" and will only work for a pod deployed by VLP

    tools_location = 'C:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe'
    command = '--cmd "info-get guestinfo.ovfenv"'
    full_command = tools_location + " " + command

    if os.path.isfile(tools_location):
        response = subprocess.run(full_command, stdout=subprocess.PIPE)
        byte_response = response.stdout
        txt_response = byte_response.decode("utf-8")

        try:
            urn = re.search('urn:vcloud:vapp:(.+?)"/>', txt_response).group(1)
        except:
            return('No urn parameter found')

        if len(urn) > 0:
            return urn
        else:
            return('No urn value found')

    else:
        return('Error: VMware tools not found')


def get_available_pod():
    # this function checks the dynamoDB to see if there are any available AWS and Azure key sets to configure the cloud accounts

    dynamodb = boto3.resource(
        'dynamodb', aws_access_key_id=d_id, aws_secret_access_key=d_sec, region_name=d_reg)
    table = dynamodb.Table('HOL-keys')

    response = table.scan(
        FilterExpression=Attr('reserved').eq(0),
        ProjectionExpression="pod, in_use"
    )
    pods = response['Items']
    # the number of pods not reserved
    num_not_reserved = len(pods)
    available_pods = 0  # set counter to zero
    pod_array = []
    for i in pods:
        if i['in_use'] == 0:  # pod is available
            available_pods += 1  # increment counter
            pod_array.append(i['pod'])

    if available_pods == 0:  # all credentials are assigned
        # get the oldest credentials and re-use those
        response = table.scan(
            FilterExpression=Attr('check_out_epoch').gt(0),
            ProjectionExpression="pod, check_out_epoch"
        )
        pods = response['Items']
        oldest = pods[0]['check_out_epoch']
        pod = pods[0]['pod']
        for i in pods:
            if i['check_out_epoch'] < oldest:
                pod = i['pod']
                oldest = i['check_out_epoch']
    else:
        # get random pod from those available
        dt = datetime.datetime.microsecond
        seed(dt)
        rand_int = randint(0, available_pods-1)
        pod = pod_array[rand_int]
    return(pod, num_not_reserved, available_pods)


def get_creds(cred_set, vlp_urn_id):

    dynamodb = boto3.resource(
        'dynamodb', aws_access_key_id=d_id, aws_secret_access_key=d_sec, region_name=d_reg)
    table = dynamodb.Table('HOL-keys')

    a = time.gmtime()  # gmt in structured format
    epoch_time = calendar.timegm(a)  # convert to epoc
    human_time = strftime("%m-%d-%Y %H:%M", a)

    # get the key set
    response = table.get_item(
        Key={
            'pod': cred_set
        }
    )
    results = response['Item']

    # write some items
    response = table.update_item(
        Key={
            'pod': cred_set
        },
        UpdateExpression="set in_use = :inuse, vlp_urn=:vlp, check_out_epoch=:out, check_out_human=:hout",
        ExpressionAttributeValues={
            ':inuse': 1,
            ':vlp': vlp_urn_id,
            ':out': epoch_time,
            ':hout': human_time
        },
        ReturnValues="UPDATED_NEW"
    )

    return(results)

def log(msg):
    if debug:
        sys.stdout.write(msg + '\n')
    file = open("C:\\hol\\vraConfig.log", "a")
    file.write(msg + '\n')
    file.close()


def send_slack_notification(payload):
    slack_url = 'https://hooks.slack.com/services/'
    post_url = slack_url + slack_api_key
    requests.post(url=post_url, proxies=proxies, json=payload)
    return()


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    results = extract(obj, arr, key)
    return results


def get_token(user_name, pass_word):
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


def get_vsphere_regions():
    api_url = '{0}iaas/api/cloud-accounts-vsphere/region-enumeration'.format(
        api_url_base)
    data = {
        "hostName": "vcsa-01a.corp.local",
        "acceptSelfSignedCertificate": "true",
        "password": "VMware1!",
        "name": "vSphere Cloud Account",
                "description": "vSphere Cloud Account",
                "username": "administrator@corp.local"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = response.json()
        regions = json_data["externalRegionIds"]
        log('- Successfully got vSphere Datacenters')
        return(regions)
    else:
        log('- Failed to get vSphere Datacenters')
        return None


def create_vsphere_ca(region_ids):
    api_url = '{0}iaas/api/cloud-accounts-vsphere'.format(api_url_base)
    data = {
        "hostName": "vcsa-01a.corp.local",
        "acceptSelfSignedCertificate": "true",
        "password": "VMware1!",
        "createDefaultZones": "true",
        "name": "Private Cloud",
                "description": "vSphere Cloud Account",
                "regionIds": region_ids,
                "username": "administrator@corp.local",
                "tags": [
                ]
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully Created vSphere Cloud Account')
    else:
        log('- Failed to Create the vSphere Cloud Account')
        return None


def create_aws_ca():
    api_url = '{0}iaas/api/cloud-accounts-aws'.format(api_url_base)
    data = {
        "description": "AWS Cloud Account",
        "accessKeyId": awsid,
        "secretAccessKey": awssec,
        "cloudAccountProperties": {

        },
        "regionIds": [
            "us-west-1"
        ],
        "tags": [
        ],
        "createDefaultZones": "true",
        "name": "AWS Cloud Account"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully Created AWS Cloud Account')
    else:
        log('- Failed to Create the AWS Cloud Account')
        return None


def create_azure_ca():
    api_url = '{0}iaas/api/cloud-accounts-azure'.format(api_url_base)
    data = {
        "name": "Azure Cloud Account",
        "description": "Azure Cloud Account",
        "subscriptionId": azsub,
        "tenantId": azten,
        "clientApplicationId": azappid,
        "clientApplicationSecretKey": azappkey,
        "regionIds": [
            "westus"
        ],
        "tags": [
        ],
        "createDefaultZones": "true"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully Created Azure Cloud Account')
    else:
        log('- Failed to create the Azure Cloud Account')
        return None


def get_czids():
    api_url = '{0}iaas/api/zones'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        cz_id = extract_values(json_data, 'id')
        return cz_id
    else:
        log('- Failed to get the cloud zone IDs')
        return None


def get_right_czid_vsphere(czid):
    api_url = '{0}iaas/api/zones/{1}'.format(api_url_base, czid)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        cz_name = extract_values(json_data, 'name')
        for x in cz_name:
            if 'RegionA01' in x:        # Looking for the CZ for vSphere
                return czid
    else:
        log('- Failed to get the right vSphere cloud zone ID')
        return None


def get_right_czid_aws(czid):
    api_url = '{0}iaas/api/zones/{1}'.format(api_url_base, czid)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        cz_name = extract_values(json_data, 'name')
        for x in cz_name:
            if x == 'AWS Cloud Account / us-west-1':
                return czid
    else:
        log('- Failed to get the right AWS cloud zone ID')
        return None


def get_right_czid_azure(czid):
    api_url = '{0}iaas/api/zones/{1}'.format(api_url_base, czid)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        cz_name = extract_values(json_data, 'name')
        for x in cz_name:
            if x == 'Azure Cloud Account / westus':
                return czid
    else:
        log('- Failed to get Azure cloud zone ID')
        return None


def get_czid_aws(czid):
    for x in czid:
        api_url = '{0}iaas/api/zones/{1}'.format(api_url_base, x)
        response = requests.get(api_url, headers=headers1, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            cz_name = extract_values(json_data, 'name')
            cz_name = cz_name[0]
            if cz_name == 'AWS-West-1 / us-west-1':
                return x
        else:
            log('- Failed to get the AWS cloud zone ID')
            return None


def get_projids():
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        proj_id = extract_values(json_data, 'id')
        return proj_id
    else:
        log('- Failed to get the project IDs')
        return None


def get_right_projid(projid):
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base, projid)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        proj_name = extract_values(json_data, 'name')
        for x in proj_name:
            if x == 'HOL Project':
                return projid
    else:
        log('- Failed to get the right project ID')
        return None


def get_right_projid_rp(projid):
    api_url = '{0}iaas/api/projects/{1}'.format(api_url_base, projid)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        proj_name = extract_values(json_data, 'name')
        for x in proj_name:
            if x == 'Rainpole Project':
                return projid
    else:
        log('- Failed to get the right project ID')
        return None


def create_project_old(vsphere, aws, azure):
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    data = {
        "name": "HOL Project",
                "zoneAssignmentConfigurations": [
                    {
                        "zoneId": vsphere,
                        "maxNumberInstances": 20,
                        "priority": 1,
                        "cpuLimit": 40,
                        "memoryLimitMB": 33554
                    },
                    {
                        "zoneId": aws,
                        "maxNumberInstances": 10,
                        "priority": 1,
                        "cpuLimit": 20,
                        "memoryLimitMB": 41943

                    },
                    {
                        "zoneId": azure,
                        "maxNumberInstances": 10,
                        "priority": 1,
                        "cpuLimit": 20,
                        "memoryLimitMB": 41943
                    }
                ],
        "administrators": [
                    {
                        "email": "holadmin"
                    }
                ],
        "members": [
                    {
                        "email": "holuser"
                    },
                    {
                        "email": "holdev"
                    }
                ],
        "machineNamingTemplate": "${resource.name}-${###}",
        "sharedResources": "true"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = response.json()
        project_id = extract_values(json_data, 'id')
        log('- Successfully created the HOL Project')
        return project_id[0]
    else:
        log('- Failed to create the HOL Project')


def create_labauto_project():
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    data = {
        "name": "Lab Automation Project",
        "administrators": [
                    {
                        "email": "holadmin"
                    }
                ],
        "sharedResources": "true"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created the Lab Automation project')
    else:
        log('- Failed to create the Lab Automation project')


def create_sd_project():
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    data = {
        "name": "Service Desk Project",
                "zoneAssignmentConfigurations": [],
        "administrators": [
                    {
                        "email": "holadmin"
                    }
                ],
        "members": [
                    {
                        "email": "holservicedesk"
                    }
                ],
        "sharedResources": "true"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created the Service Desk Project')
    else:
        log('- Failed to create the Service Desk Project')


def create_odyssey_project(vsphere, aws, azure):
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    data = {
        "name": "Odyssey Project",
                    "zoneAssignmentConfigurations": [
                        {
                        "zoneId": vsphere
                        },
                        {
                        "zoneId": aws
                        },
                        {
                        "zoneId": azure
                        }
                    ],
                    "administrators": [
                        {
                            "email": "holadmin"
                        }
                    ],
                    "members": [
                        {
                            "email": "holuser"
                        },
                        {
                            "email": "holdev"
                        }
                    ],
        "sharedResources": "true"
                }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created the Odyssey Project')
    else:
        log('- Failed to create the Odyssey Project')


def tag_vsphere_cz(cz_Ids):
    if cz_Ids is not None:
        for x in cz_Ids:
            cloudzone_id = get_right_czid_vsphere(x)
            if cloudzone_id is not None:
                api_url = '{0}iaas/api/zones/{1}'.format(
                    api_url_base, cloudzone_id)
                data = {
                    "name": "Private Cloud / RegionA01",
                            "placementPolicy": "SPREAD",
                    "tags": [
                        {
                            "key": "cloud",
                            "value": "vsphere"
                        }
                    ],
                    "tagsToMatch": [
                        {
                            "key": "compute",
                            "value": "vsphere"
                        }
                    ]
                }
                response = requests.patch(
                    api_url, headers=headers1, data=json.dumps(data), verify=False)
                if response.status_code == 200:
                    log('- Successfully Tagged vSphere Cloud Zone')
                    return(cloudzone_id)
                else:
                    log('- Failed to tag vSphere cloud zone')
                    return None
    else:
        log('- Failed to tag vSphere cloud zone')
        return None


def tag_aws_cz(cz_Ids):
    if cz_Ids is not None:
        for x in cz_Ids:
            cloudzone_id = get_right_czid_aws(x)
            if cloudzone_id is not None:
                api_url = '{0}iaas/api/zones/{1}'.format(
                    api_url_base, cloudzone_id)
                data = {
                    "name": "AWS / us-west-1",
                    "tags": [
                        {
                            "key": "cloud",
                            "value": "aws"
                        }
                    ]
                }
                response = requests.patch(
                    api_url, headers=headers1, data=json.dumps(data), verify=False)
                if response.status_code == 200:
                    log('- Successfully Tagged AWS cloud zone')
                    return cloudzone_id
                else:
                    log('- Failed to tag AWS cloud zone - bad response code')
                    return None
    else:
        log('- Failed to tag AWS cloud zone'
)
        return None


def tag_azure_cz(cz_Ids):
    if cz_Ids is not None:
        for x in cz_Ids:
            cloudzone_id = get_right_czid_azure(x)
            if cloudzone_id is not None:
                api_url = '{0}iaas/api/zones/{1}'.format(
                    api_url_base, cloudzone_id)
                data = {
                    "name": "Azure / West US",
                    "tags": [
                        {
                            "key": "cloud",
                            "value": "azure"
                        }
                    ]
                }
                response = requests.patch(
                    api_url, headers=headers1, data=json.dumps(data), verify=False)
                if response.status_code == 200:
                    log('- Successfully tagged Azure cloud zone')
                    return cloudzone_id
                else:
                    log('- Failed to tag Azure cloud zone')
                    return None
    else:
        log('- Failed to tag Azure cloud zone')
        return None


def get_azure_regionid():
    api_url = '{0}iaas/api/regions'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        region_id = extract_values(json_data, 'id')
        for x in region_id:
            api_url2 = '{0}iaas/api/regions/{1}'.format(api_url_base, x)
            response2 = requests.get(api_url2, headers=headers1, verify=False)
            if response2.status_code == 200:
                json_data2 = json.loads(response2.content.decode('utf-8'))
                region_name = extract_values(json_data2, 'externalRegionId')
                compare = region_name[0]
                if compare == 'westus':
                    region_id = extract_values(json_data2, 'id')
                    return region_id
    else:
        log('- Failed to get Azure region ID')
        return None


def create_azure_flavor():
    azure_id = get_azure_regionid()
    azure_id = azure_id[0]
    api_url = '{0}iaas/api/flavor-profiles'.format(api_url_base)
    data = {
        "name": "azure",
                "flavorMapping": {
                    "tiny": {
                        "name": "Standard_B1ls"
                    },
                    "small": {
                        "name": "Standard_B1s"
                    },
                    "medium": {
                        "name": "Standard_B1ms"
                    },
                    "large": {
                        "name": "Standard_B2s"
                    }
                },
        "regionId": azure_id
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created Azure flavor mapping')
    else:
        log('- Failed to create Azure flavor mapping')
        return None


def get_aws_regionid():
    api_url = '{0}iaas/api/regions'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        region_id = extract_values(json_data, 'id')
        for x in region_id:
            api_url2 = '{0}iaas/api/regions/{1}'.format(api_url_base, x)
            response2 = requests.get(api_url2, headers=headers1, verify=False)
            if response2.status_code == 200:
                json_data2 = json.loads(response2.content.decode('utf-8'))
                region_name = extract_values(json_data2, 'externalRegionId')
                compare = region_name[0]
                if compare == 'us-west-1':
                    aws_region_id = extract_values(json_data2, 'id')
                    return aws_region_id
    else:
        log('- Failed to get AWS region')
        return None


def create_aws_flavor():
    aws_id = get_aws_regionid()
    aws_id = aws_id[0]
    api_url = '{0}iaas/api/flavor-profiles'.format(api_url_base)
    data = {
        "name": "aws-west-1",
                "flavorMapping": {
                    "tiny": {
                        "name": "t2.nano"
                    },
                    "small": {
                        "name": "t2.micro"
                    },
                    "medium": {
                        "name": "t2.small"
                    },
                    "large": {
                        "name": "t2.medium"
                    }
                },
        "regionId": aws_id
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created AWS flavors')
    else:
        log('- Failed to created AWS flavors')
        return None


def create_aws_image():
    aws_id = get_aws_regionid()
    aws_id = aws_id[0]
    api_url = '{0}iaas/api/image-profiles'.format(api_url_base)
    data = {
        "name": "aws-image-profile",
        "description": "Image Profile for AWS Images",
        "imageMapping": {
            "CentOS7": {
                "name": "ami-a83d0cc8"
            },
            "Ubuntu18": {
                "name": "ami-0d705db840ec5f0c5"
            }
        },
        "regionId": aws_id
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created AWS images')
    else:
        log('- Failed to created AWS images')
        return None


def create_azure_image():
    azure_id = get_azure_regionid()
    azure_id = azure_id[0]
    api_url = '{0}iaas/api/image-profiles'.format(api_url_base)
    data = {
        "name": "azure-image-profile",
        "description": "Image Profile for Azure Images",
        "imageMapping": {
            "Ubuntu18": {
                "name": "Canonical:UbuntuServer:18.04-LTS:latest"
            },
            "CentOS7": {
                "name": "OpenLogic:CentOS:7.4:7.4.20180704"
            }
        },
        "regionId": azure_id
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created Azure images')
    else:
        log('- Failed to created Azure images')
        return None


def get_computeids():
    api_url = '{0}iaas/api/fabric-computes'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        comp_id = extract_values(json_data, 'id')
    return(comp_id)


def tag_vsphere_clusters(computes):
    for x in computes:
        api_url = '{0}iaas/api/fabric-computes/{1}'.format(api_url_base, x)
        response = requests.get(api_url, headers=headers1, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            cluster = extract_values(json_data, 'name')
            if "Workload" in cluster[0]:
                ## This is a vSphere workload cluster - tag it ##
                data = {
                    "tags": [
                        {
                            "key": "compute",
                            "value": "vsphere"
                        }
                    ]
                }
                response1 = requests.patch(
                    api_url, headers=headers1, data=json.dumps(data), verify=False)
                if response1.status_code == 200:
                    msg = "- Tagged " + cluster[0] + " cluster"
                    log(msg)
                else:
                    msg = "- Failed to tag: " + cluster[0] + " cluster"
                    log(msg)

        else:
            log('Failed to tag vSphere workload clusters')
    return None


def add_github_integration():
    # adds GitHub as an integration endpoint
    api_url = '{0}provisioning/uerp/provisioning/mgmt/endpoints?external'.format(
        api_url_base)
    data = {
        "endpointProperties": {
            "url": "https://api.github.com",
            "privateKey": github_key,
            "dcId": "onprem"
        },
        "customProperties": {
            "isExternal": "true"
        },
        "endpointType": "com.github.saas",
        "associatedEndpointLinks": [],
        "name": "HOL Lab Files",
        "tagLinks": []
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        json_data = response.json()
        integrationSelfLink = json_data["documentSelfLink"]
        integrationId = re.findall(
            r"([0-9A-F]{8}[-]?(?:[0-9A-F]{4}[-]?){3}[0-9A-F]{12})", integrationSelfLink, re.IGNORECASE)[0]
        log('- Successfully added GitHub integration endpoint')
        return(integrationId)
    else:
        log('- Failed to add GitHub integration endpoint')


def configure_github(projId, gitId):
    # adds GitHub blueprint integration with the HOL Project
    api_url = '{0}content/api/sources'.format(api_url_base)
    data = {
        "name": "GitHub CS",
        "typeId": "com.github",
        "syncEnabled": "true",
        "projectId": projId,
        "config": {
            "integrationId": gitId,
            "repository": "vrealize-hol/hol-2121-lab-files",
            "path": "blueprints",
            "branch": "sandbox",
            "contentType": "blueprint"
        }
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully added blueprint repo to project')
    else:
        log('- Failed to add the blueprint repo to project')


def get_fabric_network_ids():
    api_url = '{0}iaas/api/fabric-networks-vsphere'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        net_ids = extract_values(json_data, 'id')
    return(net_ids)


def update_networks(net_ids):
    for x in net_ids:
        api_url = '{0}iaas/api/fabric-networks-vsphere/{1}'.format(
            api_url_base, x)
        response = requests.get(api_url, headers=headers1, verify=False)
        if response.status_code == 200:
            json_data = response.json()
            network = extract_values(json_data, 'name')
            if "VM-Region" in network[0]:
                ## This is the vSphere VM network - update it ##
                data = {
                    "isDefault": "true",
                    "domain": "corp.local",
                    "defaultGateway": "192.168.110.1",
                    "dnsServerAddresses": ["192.168.110.10"],
                    "cidr": "192.168.110.0/24",
                            "dnsSearchDomains": ["corp.local"],
                            "tags": [
                                {
                                    "key": "net",
                                    "value": "vsphere"
                                }
                    ]
                }
                response1 = requests.patch(
                    api_url, headers=headers1, data=json.dumps(data), verify=False)
                if response1.status_code == 200:
                    log("- Updated the " + network[0] + " network")
                    return(x)
                else:
                    log("- Failed to update " + network[0] + " network")
                    return None

        else:
            log('Failed to get vSphere networks')
    return None


def create_ip_pool():
    api_url = '{0}iaas/api/network-ip-ranges'.format(api_url_base)
    data = {
        "ipVersion": "IPv4",
        "fabricNetworkId": vm_net_id,
        "name": "vSphere Static Pool",
                "description": "For static IP assignment to deployed VMs",
                "startIPAddress": "192.168.110.225",
                "endIPAddress": "192.168.110.254"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created the IP pool')
    else:
        log('- Failed to create the IP pool')
    return None


def get_vsphere_region_id():
    api_url = '{0}iaas/api/regions'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        content = json_data["content"]
        count = json_data["totalElements"]
        for x in range(count):
            # Looking to match the vSphere datacenter name
            if 'RegionA01' in content[x]["name"]:
                vsphere_id = (content[x]["id"])
                return vsphere_id
    else:
        log('- Failed to get the vSphere region (datacenter) ID')
        return None


def create_net_profile():
    api_url = '{0}iaas/api/network-profiles'.format(api_url_base)
    data = {
        "regionId": vsphere_region_id,
        "fabricNetworkIds": [vm_net_id],
        "name": "vSphere Networks",
                "description": "vSphere networks where VMs will be deployed",
                "tags": [
                    {
                        "key": "net",
                        "value": "vsphere"
                    }
        ]
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created the network profile')
    else:
        log('- Failed to create the network profile')
        return None


def get_vsphere_datastore_id():
    api_url = '{0}iaas/api/fabric-vsphere-datastores'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        content = json_data["content"]
        count = json_data["totalElements"]
        for x in range(count):
            # Looking to match the right datastore name
            if 'ISCSI01' in content[x]["name"]:
                vsphere_ds = (content[x]["id"])
                return vsphere_ds
    else:
        log('- Failed to get the vSphere datastore ID')
        return None


def create_storage_profile():
    api_url = '{0}iaas/api/storage-profiles-vsphere'.format(api_url_base)
    data = {
        "regionId": vsphere_region_id,
        "datastoreId": datastore,
        "name": "vSphere Storage",
                "description": "vSphere shared datastore where VMs will be deployed",
                "sharesLevel": "normal",
                "diskMode": "dependent",
                "provisioningType": "thin",
                "defaultItem": "true",
                "tags": [
                            {
                                "key": "storage",
                                "value": "vsphere"
                            }
                ]
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully created the storage profile')
    else:
        log('- Failed to create the storage profile')
        return None


def get_pricing_card():
    api_url = '{0}price/api/private/pricing-cards'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        content = json_data["content"]
        count = json_data["totalElements"]
        for x in range(count):
            # Looking to match the Default pricing card
            if 'Default Pricing' in content[x]["name"]:
                id = (content[x]["id"])
                return id
    else:
        log('- Failed to get default pricing card')
        return None

def sync_price():
    url = f"{api_url_base}price/api/sync-price-task"
    response = requests.request(
        "POST", url, headers=headers1, data=json.dumps({}), verify=False)
    if response.status_code == 202:
        log('- Successfully synced prices')
    else:
        log(f'- Failed to sync prices ({response.status_code})')

def modify_pricing_card(cardid):
    # modifies the Default Pricing card
    api_url = '{0}price/api/private/pricing-cards/{1}'.format(
        api_url_base, cardid)
    data = {
        "name": "HOL Pricing Card",
        "description": "Sets pricing rates for vSphere VMs",
        "meteringItems": [
            {
                "itemName": "vcpu",
                "metering": {
                    "baseRate": 29,
                    "chargePeriod": "MONTHLY",
                    "chargeOnPowerState": "ALWAYS",
                    "chargeBasedOn": "USAGE"
                }
            },
            {
                "itemName": "memory",
                "metering": {
                    "baseRate": 85,
                    "chargePeriod": "MONTHLY",
                    "chargeOnPowerState": "ALWAYS",
                    "chargeBasedOn": "USAGE",
                    "unit": "gb"
                },
            },
            {
                "itemName": "storage",
                "metering": {
                    "baseRate": 0.14,
                    "chargePeriod": "MONTHLY",
                    "chargeOnPowerState": "ALWAYS",
                    "chargeBasedOn": "USAGE",
                    "unit": "gb"
                }
            }
        ],
        "chargeModel": "PAY_AS_YOU_GO"
    }
    response = requests.put(api_url, headers=headers1,
                            data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('- Successfully modified the pricing card')
    else:
        log('- Failed to modify the pricing card')


def get_blueprint_id(bpName):
    api_url = '{0}blueprint/api/blueprints'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        content = json_data["content"]
        count = json_data["totalElements"]
        for x in range(count):
            if bpName in content[x]["name"]:  # Looking to match the blueprint name
                bp_id = (content[x]["id"])
                return bp_id
    else:
        log('- Failed to get the blueprint ID for ' + bpName)
        return None


def release_blueprint(bpid, ver):
    api_url = '{0}blueprint/api/blueprints/{1}/versions/{2}/actions/release'.format(
        api_url_base, bpid, ver)
    data = {}
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('- Successfully released the blueprint')
    else:
        log('- Failed to releasea the blueprint')


def add_bp_cat_source(projid):
    # adds blueprints from 'projid' project as a content source
    api_url = '{0}catalog/api/admin/sources'.format(api_url_base)
    data = {
        "name": "HOL Project Blueprints",
        "typeId": "com.vmw.blueprint",
        "description": "Released blueprints in the HOL Project",
        "config": {"sourceProjectId": projid},
        "projectId": projid
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = response.json()
        sourceId = json_data["id"]
        log('- Successfully added blueprints as a catalog source')
        return sourceId
    else:
        log('- Failed to add blueprints as a catalog source')
        return None


def share_bps(source, project):
    # shares blueprint content (source) from 'projid' project to the catalog
    api_url = '{0}catalog/api/admin/entitlements'.format(api_url_base)
    data = {
        "definition": {"type": "CatalogSourceIdentifier", "id": source},
        "projectId": project
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('- Successfully added blueprint catalog entitlement')
    else:
        log('- Failed to add blueprint catalog entitlement')
        return None


def get_cat_id(item_name):
    api_url = '{0}catalog/api/items'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        content = json_data["content"]
        count = json_data["totalElements"]
        for x in range(count):
            # Looking to match the named catalog item
            if item_name in content[x]["name"]:
                cat_id = (content[x]["id"])
                return cat_id
    else:
        log('- Failed to get the blueprint ID')
        return None


def deploy_cat_item(catId, project):
    # shares blueprint content (source) from 'projid' project to the catalog
    api_url = '{0}catalog/api/items/{1}/request'.format(api_url_base, catId)
    data = {
        "deploymentName": "vSphere Ubuntu",
        "projectId": project,
        "version": "1",
        "reason": "Deployment of vSphere vm from blueprint",
        "inputs": {}
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('- Successfully deployed the catalog item')
    else:
        log('- Failed to deploy the catalog item')


def check_for_assigned(vlpurn):
    # this function checks the dynamoDB to see if this pod urn already has a credential set assigned

    dynamodb = boto3.resource(
        'dynamodb', aws_access_key_id=d_id, aws_secret_access_key=d_sec, region_name=d_reg)
    table = dynamodb.Table('HOL-keys')

    response = table.scan(
        FilterExpression="attribute_exists(vlp_urn)",
        ProjectionExpression="pod, vlp_urn"
    )
    urns = response['Items']
    urn_assigned = False
    for i in urns:
        if i['vlp_urn'] == vlpurn:  # This URN already has a key assigned
            urn_assigned = True

    return(urn_assigned)


def getOrg(headers):
    url = f"{api_url_base}csp/gateway/am/api/loggedin/user/orgs"
    response = requests.request(
        "GET", url, headers=headers, verify=False)
    return response.json()['items'][0]['id']


def getEndpoints(headers):
    url = f"{api_url_base}provisioning/uerp/provisioning/mgmt/endpoints?expand"
    response = requests.request("GET", url, headers=headers, verify=False)
    if response.status_code == 200:
        log("- Successfully retrieved endpoint list")    
        endpointList = {}
        for endpoint_link in response.json()['documentLinks']:
            endpoint = response.json()['documents'][endpoint_link]
            endpointList[endpoint['endpointType']] = endpoint['documentSelfLink']
        return endpointList


def addCustomResource(headers, vro_endpoint, resource_file):
    resource_content = json.loads(open(resource_file).read())
    resource_content['mainActions']['create']['endpointLink'] = vro_endpoint
    resource_content['mainActions']['delete']['endpointLink'] = vro_endpoint

    url = f"{api_url_base}form-service/api/custom/resource-types"
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(resource_content), verify=False)
    if response.status_code == 200:
        log("- Successfully added Custom Resource")
    else:
        log(f"- Failed to add Custom Resource ({response.status_code})")


def addResourceAction(headers, vro_endpoint, org, resource_file):
    resource_content = json.loads(open(resource_file).read())
    resource_content['runnableItem']['endpointLink'] = vro_endpoint
    resource_content['orgId'] = org
    resource_content['formDefinition']['tenant'] = org

    url = f"{api_url_base}form-service/api/custom/resource-actions"
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(resource_content), verify=False)
    if response.status_code == 200:
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(resource_content), verify=False)
        if response.status_code == 200:
            log("- Successfully added Custom Action")
        else:
            log(f"- Failed to add Custom Action ({response.status_code})")
    else:
        log(f"- Failed to add Custom Action ({response.status_code})")


def create_approval_policy(catId, projId):
    # creates an approval policy
    api_url = '{0}policy/api/policies'.format(api_url_base)
    data = {
        "name" : "Azure approval",
        "description" : "Approval policy for a catalog item that deploys to Azure",
        "typeId" : "com.vmware.policy.approval",
        "enforcementType" : "HARD",
        "projectId" : projId,
        "definition" : {
            "level" : 1,
            "approvalMode" : "ANY_OF",
            "autoApprovalDecision" : "APPROVE",
            "approvers" : [
                "USER:holadmin"
                ],
            "autoApprovalExpiry" :1,
            "actions" :[
                "Deployment.Create"
                ]
            },
        "criteria" :{
            "matchExpression" :[
                {
                    "key" :"catalogItemId",
                    "operator" :"eq",
                    "value" :catId
                }
            ]
        }
    }
    response = requests.post(api_url, headers=headers1, data=json.dumps(data) ,verify=False)
    if response.status_code == 201:
        log('- Successfully created the approval policy')
    else:
        log('- Failed to create the approval policy')


def create_cs_endpoint():
    # creates a dummy code stream endpoint for the chat app pipeline example
    api_url = '{0}codestream/api/endpoints'.format(api_url_base)
    data = {
        "name": "Ent PKS Prod",
        "description": "Dummy endpoint for chat app pipeline",
        "isRestreicted": "",
        "project": "HOL Project",
        "type": "k8s",
        "properties": {
            "kubernetesURL": "http://1.2.3.4",
            "authType": "basicAuth",
            "userName": "holuser",
            "password": "VMware1!"
        }
    }
    response = requests.post(api_url, headers=headers1, data=json.dumps(data) ,verify=False)
    if response.status_code == 200:
        log('- Successfully created the code stream endpoint')
    else:
        log('- Failed to create the code stream endpoint')


def import_pipelines(pipeNames):
    # imports code stream pipelines contained in the array of names
    api_url = '{0}codestream/api/import'.format(api_url_base)
    count = len(pipeNames)
    for i in range(count):
        fname = pipeNames[i]
        fileName = 'C:/hol-2121-lab-files/automation/' + fname + '.yaml'
        file = open(fileName, 'r')
        payload = file.read()
        response = requests.post(api_url, headers=headers2, data=payload, verify=False)
        if response.status_code == 200:
            log('- Imported' + fname + 'pipeline')
        else:
            log('- Failed to imort' + fname + 'pipeline')


def get_pipelines():
    # returns an array containing all of the pipeline ids
    api_url = '{0}codestream/api/pipelines'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        Ids = extract_values(json_data, 'id')
        return Ids
    else:
        log('- Failed to get pipelines')
        return None


def enable_pipelines(Ids):
    # enables all pipelines the array
    count = len(Ids)
    data = { "enabled": "true"}
    for i in range(count):
        api_url = '{0}codestream/api/pipelines/{1}'.format(api_url_base, Ids[i])
        response = requests.patch(api_url, headers=headers1, data=json.dumps(data), verify=False)
        if response.status_code == 200:
            log('- Enabled pipeline')
        else:
            log('- Failed to enable pipeline')

def is_configured():
    # checks to see if vRA is already configured
    api_url = '{0}iaas/api/cloud-accounts'.format(api_url_base)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        caTypes = extract_values(json_data, 'cloudAccountType')
        for x in caTypes:
            if 'azure' in x: 
                return True
        return False
    else:
        log('Could not get cloud accounts')


def get_gitlab_projects():
    # returns an array containing all of the project ids
    api_url = '{0}projects{1}'.format(gitlab_api_url_base, gitlab_token_suffix)
    response = requests.get(api_url, headers=gitlab_header, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        for project in json_data:
            if 'dev' in project['name']:        # looking for the 'dev' project
                return project['id']
        else:
            log('- Did not find the dev gitlab project')
    else:
        log('- Failed to get gitlab projects')


def update_git_proj(projId):
    # sets the visibility of the passed project ID to public
    api_url = '{0}projects/{1}{2}'.format(gitlab_api_url_base, projId, gitlab_token_suffix)
    data = {
        "visibility": "public"
    }
    response = requests.put(api_url, headers=gitlab_header, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        log('- Updated the gitlab project')
    else:
        log('- Failed to update the gitlab project')



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
            if result['displayName'] == groupName:
                found = True
        return(found)

def getAvailableEnterpriseGroups(searchString):
    api_url = '{0}csp/gateway/am/api/groups/search?searchTerm={1}'.format(api_url_base, searchString)
    response = requests.get(api_url, headers=headers1, verify=False)
    if response.status_code == 200:
        content = response.json()
        resultCount = content['totalResults']
        if resultCount == 1:
            groupId = content['results'][0]['id']
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
                        "email": "web-dev-team@corp.local"
                    }
                ],
        "machineNamingTemplate": "${resource.name}${####}",
        "sharedResources": "false"
    }
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        json_data = response.json()
        project_id = extract_values(json_data, 'id')
        log('Successfully created the Project')
        return project_id[0]
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
    response = requests.post(api_url, headers=headers1,
                             data=json.dumps(data), verify=False)
    if response.status_code == 201:
        log('Successfully added cloud template repo to project')
    else:
        log('Failed to add the cloud template repo to project. Exiting ...')
        quit()

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
    else:
        log('Failed to find the cloud template named ' + ctName + '. Exiting ...')
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
    else:
        log('Failed to get the ID of the content item. Exiting ...')
        quit()


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
groupName = 'web-dev-team@corp.local'
if checkEnterpriseGroups(groupName):
    logMessage = groupName + ' group already exists in vRA'
    log(logMessage)
else:
    log('Did not find the {0} group in vRA. Adding it.'.format(groupName))
    id = getAvailableEnterpriseGroups('web-dev')
    setGroupRoles(id)

# Add the project to Cloud Assembly
projId = createProject()

# Add the GitHub cloud template repo to the project
configureGithub(projId)

# Update the ABX action
updateABX()

# Update the subscription
updateSubscription(projId)

# Pause to give time for cloud templates to sync from GitLab
log('Pausing to give time for cloud templates to sync from GitLab')
time.sleep(20)

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


"""
##########################################
# CONFIGURE vRSLCM
##########################################
log('*** Configuring vRSLCM')

api_url_base = 'https://' + vrslcm_fqdn + '/lcm/authzn/api/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
            'Authorization': 'Basic YWRtaW5AbG9jYWw6Vk13YXJlMSE='}
#vrslcmLogin("admin@local", "VMware1!")

#addAdGroup()
syncAdGroup()


