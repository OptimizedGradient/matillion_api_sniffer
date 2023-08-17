import requests
from requests.auth import HTTPBasicAuth
import os
import json
import time
import csv

# ------------------------------------------------------------------------------
# get environment variables
# ------------------------------------------------------------------------------
api_user     = os.environ['MATILLION_API_USER']     # error if no value, API username to connect to Matillion
api_pass     = os.environ['MATILLION_API_PASS']     # error if no value, API password to connect to Matillion
api_base     = os.environ['MATILLION_API_BASE']     # error if no value, base url to connect to

print(f"""
Configuration:
api_base: {api_base}
""")
# ------------------------------------------------------------------------------

def call_api(url, user, user_pass):
    """
    Calls Matillion Job
    """
    # trigger api
    print(f'Triggering job:\n\turl: {url}')
    run_job_resp = requests.get(url, auth=HTTPBasicAuth(user, user_pass)).text
    json_resp = json.loads(run_job_resp)

    return json_resp


def get_groups():
    """
    Calls Matillion to list groups
    """
    url = """{api_base}/rest/v1/group""".format(api_base=api_base)
    json_response = call_api(url, api_user, api_pass)

    return json_response


def get_projects(group_name):
    """
    Calls Matillion to list projects
    """
    url = """{api_base}/rest/v1/group/name/{group_name}/project""".format(api_base=api_base,group_name=group_name)
    json_response = call_api(url, api_user, api_pass)

    return json_response


def get_versions(group_name, project_name):
    """
    Calls Matillion to look at versions
    """
    url = """{api_base}/rest/v1/group/name/{group_name}/project/name/{project_name}/version""".format(api_base=api_base,group_name=group_name,project_name=project_name)
    json_response = call_api(url, api_user, api_pass)

    return json_response


def get_jobs(group_name, project_name, version_name):
    """
    Calls Matillion to look at jobs
    """
    url = """{api_base}/rest/v1/group/name/{group_name}/project/name/{project_name}/version/name/{version_name}/job""".format(api_base=api_base,group_name=group_name,project_name=project_name,version_name=version_name)
    json_response = call_api(url, api_user, api_pass)

    return json_response


def get_job_details(group_name, project_name, version_name, job_name):
    """
    Calls Matillion to look at job
    """
    url = """{api_base}/rest/v1/group/name/{group_name}/project/name/{project_name}/version/name/{version_name}/job/name/{job_name}/export""".format(api_base=api_base,group_name=group_name,project_name=project_name,version_name=version_name,job_name=job_name)
    json_response = call_api(url, api_user, api_pass)

    return json_response



def main():
    print('Beginning scan of Matillion instance...')
    # set list
    lv_output = []
    # get groups
    lv_groups = get_groups()

    # loop through groups
    for group in lv_groups:
        # get the projects for the group
        projects = get_projects(group)
        # loop through projects
        for project in projects:
            # get the versions
            versions = get_versions(group, project)
            # loop through versions
            for version in versions:
                # get jobs
                jobs = get_jobs(group, project, version)
                # loop through jobs
                for job in jobs:
                    lv_sql_cnt = 0
                    # get job specifics
                    job_details = get_job_details(group, project, version, job)
                    # loop through component in job
                    for object in job_details["objects"]:
                        for component in object["jobObject"]["components"]:
                            for parameter in object["jobObject"]["components"][component]["parameters"]:
                                if object["jobObject"]["components"][component]["parameters"][parameter]["name"] == "SQL Query":
                                    lv_sql_cnt += 1
                    print("""Group: {group}\nProject: {project}\nVersion: {version}\nJob: {job}\nSQL Count: {sql_cnt}""".format(group=group,project=project,version=version,job=job,sql_cnt=lv_sql_cnt))
                    dict = {"group": group, "project": project, "version": version, "job": job, "sql_cnt": lv_sql_cnt}
                    lv_output.append(dict)
    print('Finished scanning Matillion!')
    print('Writing CSV report...')
    fields = ["group", "project", "version", "job", "sql_cnt"]
    with open('output.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(lv_output)
    print('Finished writing CSV report!')

if __name__ == "__main__":
    main()
