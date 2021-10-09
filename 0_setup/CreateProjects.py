# Initial setup for future project samples
# Create root "tsx-examples" project
# Create two Human Resource projects under "tsx-examples" project

import tableauserverclient as TSC
import os
from dotenv import load_dotenv, find_dotenv

def getCredentials(env):
    load_dotenv(find_dotenv(env))
    return os.environ.get('tokenName'), os.environ.get('tokenSecret'), os.environ.get('url'), os.environ.get('site')

def createProject(project_name, parent_id=None):
    # New project item
    new_project = TSC.ProjectItem(name=project_name, content_permissions='LockedToProjectWithoutNested', description='Project for tsc-example', parent_id=parent_id)
    # Create project on site
    new_project = server.projects.create(new_project)
    return new_project.id

if __name__ == '__main__':
    # Grab credentials from env file
    tokenName, tokenSecret, serverurl, sitename = getCredentials('.env')

    tableau_auth = TSC.PersonalAccessTokenAuth(tokenName, tokenSecret, sitename)
    server = TSC.Server(serverurl)

    # Create root project name
    project_parent = "tsc-examples"
    # Create list of child projects
    project_children = ["Human Resources", "Human Resources - UAT"]

    # Sign into server
    with server.auth.sign_in(tableau_auth):
        server.use_server_version()
        print('Signed in . . .')
        # Generate root project
        parent_id = createProject(project_parent)
        # Create child projects nested under parent
        for project in project_children:
            createProject(project, parent_id)

    print('Created sample projects!')
