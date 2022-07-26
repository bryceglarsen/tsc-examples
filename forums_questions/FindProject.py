import tableauserverclient as TSC
import argparse
import os
import sys
from dotenv import load_dotenv, find_dotenv

def getCredentials(env):
    load_dotenv(find_dotenv(env))
    return os.environ.get('tokenName'), os.environ.get('tokenSecret'), os.environ.get('url'), os.environ.get('site')
    
def getProjects(name, parentIds=[]):
    # return all matches in case same project name
    if len(parentIds) > 0:
        return [project for project in TSC.Pager(server.projects) if project.name == name and project.parent_id in parentIds]
    return [project for project in TSC.Pager(server.projects) if project.name == name]
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='View permissions per project')
    parser.add_argument('--projectName', '-p', required=True, help='project name')
    parser.add_argument('--parentName', '-pp', required=False, help='parent project name')

    args = parser.parse_args()
    projectName = args.projectName
    parentName = args.parentName
    # Grab credentials from env file
    tokenName, tokenSecret, serverurl, sitename = getCredentials('.env')

    tableau_auth = TSC.PersonalAccessTokenAuth(tokenName, tokenSecret, sitename)
    server = TSC.Server(serverurl)

    # Sign into server
    with server.auth.sign_in(tableau_auth):
        server.use_server_version()
        parentIds = []
        if parentName:
            parentProjects = getProjects(parentName)
            if len(parentProjects) == 0:
                sys.exit("No Projects Match Supplied Parent Name")
            parentIds = [project.id for project in parentProjects]

        projects = getProjects(projectName, parentIds)
        for prj in projects:
            print(f'{prj.name}: ({prj.id})')