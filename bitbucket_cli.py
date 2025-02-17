import click
import os
import oauth_authentication
import requests
import json

BITBUCKET_BASE_URL="https://api.bitbucket.org/2.0"
##########Currently it is not possible to access the permission config API using Workspace Access Tokens (WAT)
##########so this credentials need to be used:
BITBUCKET_USERNAME=os.getenv("BITBUCKET_USERNAME")
BITBUCKET_PASSWORD=os.getenv("BITBUCKET_PASSWORD")
############################################
user_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_headers():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {oauth_authentication.authenticate()}"
    }
    return headers

def post_request(request_url, request_json):
    response = requests.request("POST", request_url, json=request_json, headers=get_headers())
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def post_creds_request(request_url, request_json):
    response=requests.request("POST", request_url, json=request_json, headers=user_headers,auth=(BITBUCKET_USERNAME,BITBUCKET_PASSWORD))
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def put_creds_request(request_url, request_json):
    response=requests.request("PUT", request_url, json=request_json, headers=user_headers,auth=(BITBUCKET_USERNAME,BITBUCKET_PASSWORD))
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def delete_creds_request(request_url):
    response=requests.request("DELETE", request_url, auth=(BITBUCKET_USERNAME,BITBUCKET_PASSWORD))
    print(response.text)

@click.group()
def cli():
    pass

@click.command()
@click.argument("workspace")
@click.argument("json_file", type=click.File("r"))
def create_project(workspace,json_file):
    url=f"{BITBUCKET_BASE_URL}/workspaces/{workspace}/projects"
    payload=json.load(json_file)
    post_request(url, payload)

@click.command()
@click.argument("workspace")
@click.argument("repo_slug")
@click.argument("json_file", type=click.File("r"))
def create_repository(workspace, repo_slug, json_file):
    url=f"{BITBUCKET_BASE_URL}/repositories/{workspace}/{repo_slug}"
    payload=json.load(json_file)
    post_request(url, payload)

@click.command()
@click.argument("workspace")
@click.argument("repo_slug")
@click.argument("selected_user_id")
@click.argument("json_file", type=click.File("r"))
def add_user(workspace, repo_slug, selected_user_id, json_file):
    url=f"{BITBUCKET_BASE_URL}/repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id}"
    payload=json.load(json_file)
    put_creds_request(url, payload)

@click.command()
@click.argument("workspace")
@click.argument("repo_slug")
@click.argument("selected_user_id")
def del_user(workspace, repo_slug, selected_user_id):
    url=f"{BITBUCKET_BASE_URL}/repositories/{workspace}/{repo_slug}/permissions-config/users/{selected_user_id}"
    delete_creds_request(url)

@click.command()
@click.argument("workspace")
@click.argument("repo_slug")
@click.argument("json_file", type=click.File("r"))
def branch_restriction_rule(workspace, repo_slug, json_file):
    url=f"{BITBUCKET_BASE_URL}/repositories/{workspace}/{repo_slug}/branch-restrictions"
    payload=json.load(json_file)
    post_creds_request(url,payload)


cli.add_command(create_project)
cli.add_command(create_repository)
cli.add_command(add_user)
cli.add_command(del_user)
cli.add_command(branch_restriction_rule)
if __name__== '__main__':
    cli()