import tableauserverclient as TSC
import argparse
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv, find_dotenv

def getCredentials(env):
    load_dotenv(find_dotenv(env))
    return os.environ.get('tokenName'), os.environ.get('tokenSecret'), os.environ.get('url'), os.environ.get('site')
    
def getPermissions(workbook, output):
    server.workbooks.populate_permissions(workbook)
    permissions = workbook.permissions
    if output == 'terminal':
        print(f'Permissions for {workbook.name}. . .')
    i = -1
    wb_permissions = []
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
        if output == 'terminal':
            print('Type: %s\tName: %s\tCapabilities: %s' %(group_user_type, group_user_name, group_user_capabilities))
            print('\n')
        else:
            for capability, status in group_user_capabilities.items():
                wb_permissions.append([workbook.name, group_user_type, group_user_name, capability, status])

    return wb_permissions
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='View permissions per workbook')
    parser.add_argument('--output', '-o', required=False, default='terminal', 
        choices=['terminal', 'csv'], help='ouput results to terminal window or csv file')
    # parser.add_argument('--workbookName', '-p', required=True, help='workbook area not including stage')

    args = parser.parse_args()
    output = args.output

    # Grab credentials from env file
    tokenName, tokenSecret, serverurl, sitename = getCredentials('.env')

    tableau_auth = TSC.PersonalAccessTokenAuth(tokenName, tokenSecret, sitename)
    server = TSC.Server(serverurl)

    # Sign into server
    with server.auth.sign_in(tableau_auth):
        workbooks = list(TSC.Pager(server.workbooks))
        permissions_list = []
        for workbook in workbooks:
            permissions_list.extend(getPermissions(workbook, output))
        if output == 'csv':
            permissions_df = pd.DataFrame(permissions_list, columns=['workbook', 'grantee_type', 'grantee_name', 'capability', 'status'])
            # Get current path of script
            filepath = Path(Path(__file__).parent) / 'zzzOutputs'
            filepath.mkdir(exist_ok=True)
            filename = filepath / 'WorkbookPermissions.csv'
            permissions_df.to_csv(filename, index=False)