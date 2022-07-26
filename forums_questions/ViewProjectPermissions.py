import tableauserverclient as TSC
import argparse
import os
from dotenv import load_dotenv, find_dotenv

def getCredentials(env):
    load_dotenv(find_dotenv(env))
    return os.environ.get('tokenName'), os.environ.get('tokenSecret'), os.environ.get('url'), os.environ.get('site')
    
def getPermissions(project):
    server.projects.populate_permissions(project)
    permissions = project.permissions
    i = -1
    for rule in permissions:
        i += 1
        group_user_type = permissions[i].grantee.tag_name
        group_user_id = permissions[i].grantee.id
        group_user_capabilities = permissions[i].capabilities
        if group_user_type == 'user':
            user_item = server.users.get_by_id(permissions[i].grantee.id)
            group_user_name = user_item.name
        elif group_user_type == 'group':
            for group_item in TSC.Pager(server.groups):
                if group_item.id == group_user_id:
                    group_user_name = group_item.name
                    break
        print('Type: %s\tName: %s\tCapabilities: %s' %(group_user_type, group_user_name, group_user_capabilities))
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='View permissions per project')
    parser.add_argument('--projectName', '-p', required=True, help='project area not including stage')

    args = parser.parse_args()
    projectName = args.projectName
    # Grab credentials from env file
    tokenName, tokenSecret, serverurl, sitename = getCredentials('.env')

    tableau_auth = TSC.PersonalAccessTokenAuth(tokenName, tokenSecret, sitename)
    server = TSC.Server(serverurl)

    # Sign into server
    with server.auth.sign_in(tableau_auth):
        project = [project for project in TSC.Pager(server.projects) if project.name == projectName][0]
        getPermissions(project)