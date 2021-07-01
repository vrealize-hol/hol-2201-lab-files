import sys
import requests
import json
import urllib3
urllib3.disable_warnings()

vra_fqdn = "vr-automation.corp.local"
api_url_base = "https://" + vra_fqdn + "/"
apiVersion = "2019-01-15"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def login(username, password):
    api_url = '{0}csp/gateway/am/api/login?access_token'.format(api_url_base)
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(api_url, headers=headers,
                             data=json.dumps(data), verify=False)
    if response.status_code == 200:
        api_url = '{0}iaas/api/login'.format(api_url_base)
        response = requests.post(api_url, headers=headers,
                                 data=json.dumps({"refreshToken": response.json()['refresh_token']}), verify=False)
        if response.status_code == 200:
            headers['Authorization'] = 'Bearer {0}'.format(
                response.json()['token'])
            return response.json()['token']

    return('not ready')


def get_project_id(name):
    api_url = '{0}iaas/api/projects'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200 and response.json()['content']:
        for project in response.json()['content']:
            if project['name'] == name:
                return project['id']
    print('- Failed to get the project ID for', name)
    return None


def get_blueprint_id(name):
    api_url = '{0}blueprint/api/blueprints'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200 and response.json()['content']:
        for project in response.json()['content']:
            if project['name'] == name:
                return project['id']
    print('- Failed to get the blueprint ID for', name)
    return None


def release_blueprint(blueprint_id, version):
    api_url = f"{api_url_base}blueprint/api/blueprints/{blueprint_id}/versions/{version}/actions/release"
    response = requests.post(api_url, headers=headers,
                             data=json.dumps({}), verify=False)
    if response.status_code == 200:
        print('- Successfully released the blueprint')
    else:
        print('- Failed to release the blueprint')


def unrelease_blueprint(blueprint_id, version):
    api_url = f"{api_url_base}blueprint/api/blueprints/{blueprint_id}/versions/{version}/actions/unrelease"
    response = requests.post(api_url, headers=headers,
                             data=json.dumps({}), verify=False)
    if response.status_code == 200:
        print('- Successfully unreleased the blueprint')
    else:
        print('- Failed to unrelease the blueprint')


def refresh_catalog_source(name):
    api_url = '{0}catalog/api/admin/sources'.format(api_url_base)
    response = requests.get(api_url, headers=headers, verify=False)
    if response.status_code == 200 and response.json()['content']:
        for catalog in response.json()['content']:
            if catalog['name'] == name:
                response = requests.post(api_url, data=json.dumps(
                    catalog), headers=headers, verify=False)
                if response.status_code == 201:
                    print('- Catalog refreshed', name)
                    return
    print('- Failed to refresh catalog', name)
    return None


##### MAIN #####
###########################################
# API calls below as holadmin
###########################################
access_key = login("holadmin@corp.local", "VMware1!")

if access_key == 'not ready':  # we are not even getting an auth token from vRA yet
    print('\n\n\nvRA is not yet ready in this Hands On Lab pod - no access token yet')
    print('Wait for the lab status to be *Ready* and then run this script again')
    sys.exit()

# Release the fixed blueprint version for HOL-2201-08
hol_project_id = get_project_id("HOL Project")
blueprint_id = get_blueprint_id('Distributed System')
release_blueprint(blueprint_id, 2)
unrelease_blueprint(blueprint_id, 1)
refresh_catalog_source("Web Hosting Templates")
