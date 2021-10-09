# 1. Get Credentials
# 2. Get Groups
# 3. Get Projects
# 4. Assign permissions
# 5. Assign view rights to parent folder(s)

import tableauserverclient as TSC
import pandas as pd
from pathlib import Path
import argparse
import os
from dotenv import load_dotenv, find_dotenv

def getCredentials(env):
    load_dotenv(find_dotenv(env))
    return os.environ.get('tokenName'), os.environ.get('tokenSecret'), os.environ.get('url'), os.environ.get('site')

def getGroups(grouproot):
    # Grab all groups on server using list comprehension
    # Filter by removing role suffix with rsplit
    groups = [group for group in TSC.Pager(server.groups) if group.name.rsplit(' - ', 1)[0] == grouproot]
    return groups

def getProjects(projectroot):
    # Grab all projects on server using list comprehension
    # Filter by removing stage suffix with rsplit
    projects = [project for project in TSC.Pager(server.projects) if project.name == projectroot or project.name.rsplit(' - ', 1)[0] == projectroot]
    return projects

def addToParent(project_id,  group):
    projects = [project for project in TSC.Pager(server.projects) if project.id == project_id]
    project = projects[0]
    server.projects.update_permissions(project, [TSC.PermissionsRule(grantee=group, capabilities={TSC.Permission.Capability.Read : TSC.Permission.Mode.Allow})])
    # Continue to add to all parent projects
    if project.parent_id:
        addToParent(project.parent_id, group)
    return

def assignPermissions(groups, projects):
    # Read in excel file with permissions mapping
    permissions_df = pd.read_csv('./Permissions.csv')

    # Convert text strings to TSC API
    permissions_df['CapabilityAPI'] =  permissions_df['CapabilityAPI'].apply(lambda x: eval(('TSC.Permission.Capability.' + x)))
    permissions_df['ModeAPI'] = permissions_df['ModeAPI'].apply(lambda x: eval(('TSC.Permission.Mode.' + x)))

    # Map roles to actual Groups
    # We will use this to filter the permissions dataframe
    role_to_group = {group.name.rsplit(' - ', 1)[1] : group for group in groups}

    # Loop through projects
    for project in projects:
        # Identify project stage by grabbing suffix
        if len(project.name.rsplit(' - ', 1))>1 and project.name.rsplit(' - ', 1)[1] in ['UAT']:
            project_stage = project.name.rsplit(' - ', 1)[1]
        else:
            project_stage = 'PROD'

        # Filter permissions table by stage and relevant roles
        project_permissions = permissions_df.loc[(permissions_df.ProjectStageDSC == project_stage) & (permissions_df.RoleTypeDSC.isin(role_to_group))]

        # Create dictionary mapping role & object type to capabilities/permissions
        # We want permissions in a dictionary to pass to the method
        # (role, object) : permissions
        object_to_permissions = {
            area : dict(zip(permissions.CapabilityAPI, permissions.ModeAPI))
            for area, permissions in project_permissions.groupby(['RoleTypeDSC', 'ObjectTypeDSC'])
            }

        for area, permissions in object_to_permissions.items():
            group = role_to_group.get(area[0])
            object = area[1]

            if object == 'Project':
                server.projects.update_permissions(project, [TSC.PermissionsRule(grantee=group, capabilities=permissions)])
                # Add view permission to parent project(s)
                if project.parent_id:
                    addToParent(project.parent_id, group)
            if object == 'Workbook':
                server.projects.update_workbook_default_permissions(project, [TSC.PermissionsRule(grantee=group, capabilities=permissions)])
            if object == 'Datasource':
                server.projects.update_datasource_default_permissions(project, [TSC.PermissionsRule(grantee=group, capabilities=permissions)])

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assign group permissions per project')
    parser.add_argument('--grouproot', '-g', required=True, help='group name not including role')
    parser.add_argument('--projectroot', '-p', required=True, help='project area not including stage')

    args = parser.parse_args()
    # Grab credentials from env file
    tokenName, tokenSecret, serverurl, sitename = getCredentials('.env')

    tableau_auth = TSC.PersonalAccessTokenAuth(tokenName, tokenSecret, sitename)
    server = TSC.Server(serverurl)

    # Sign into server
    with server.auth.sign_in(tableau_auth):
        server.use_server_version()

        groups = getGroups(args.grouproot)
        projects = getProjects(args.projectroot)
        assignPermissions(groups, projects)
        print('Added {} \nto {}!'.format(', '.join([group.name for group in groups]), ', '.join([project.name for project in projects])))
