import tableauserverclient as TSC
import os
from dotenv import load_dotenv, find_dotenv

def getCredentials(env):
    load_dotenv(find_dotenv(env))
    return os.environ.get('tokenName'), os.environ.get('tokenSecret'), os.environ.get('url'), os.environ.get('site')

def createGroup(group):
    # New project item
    new_group = TSC.GroupItem(group)
    # Create project on site
    new_project = server.groups.create(new_group)
    return

if __name__ == '__main__':
    # Grab credentials from env file
    tokenName, tokenSecret, serverurl, sitename = getCredentials('.env')

    tableau_auth = TSC.PersonalAccessTokenAuth(tokenName, tokenSecret, sitename)
    server = TSC.Server(serverurl)

    # Create root project name
    group_names = ["HR - Super Users", "HR - Developers", "HR - Viewers"]

    # Sign into server
    with server.auth.sign_in(tableau_auth):
        server.use_server_version()
        print('Signed in . . .')

        # Create child projects nested under parent
        for group in group_names:
            createGroup(group)

    print('Created sample groups!')
