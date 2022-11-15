# 1. Get Credentials
# 2. Get Groups
# 3. Get Projects
# 4. Assign permissions
# 5. Assign view rights to parent folder(s)

import tableauserverclient as TSC
from pathlib import Path
import os
from datetime import date
from dotenv import load_dotenv, find_dotenv

def getCredentials(env):
    load_dotenv(find_dotenv(env))
    return os.environ.get('tokenName'), os.environ.get('tokenSecret'), os.environ.get('url'), os.environ.get('site')

def main():
    # get today's date as text
    today = date.today().strftime('%Y%m%d')
    # define folder name
    currentfolder = Path(__file__).parent.absolute()
    imgfolder = Path.joinpath(currentfolder, f'zViewImages/{today}')
    
    # get all workbooks
    # you can add filter criteria here if desired to exclude by name, project, author, etc.
    all_workbooks = list(TSC.Pager(server.workbooks))

    # loop through all workbooks
    for wb in all_workbooks:
        # create workbook folder
        wbfolder = Path.joinpath(imgfolder, wb.project_name, wb.name)
        Path(wbfolder).mkdir(parents=True, exist_ok=True)

        # get all views per current workbook
        wb_views = [views for views in TSC.Pager(server.views) if views.workbook_id == wb.id]
        for view in wb_views:
            # if needed, set resolution to hight
            #image_req_option = TSC.ImageRequestOptions(imageresolution=TSC.ImageRequestOptions.Resolution.High)
            try:
                server.views.populate_image(view) #, image_req_option)
                filename = wb.name + '~' + view.name + '.png'
                print(filename)
                with open(wbfolder + '/' + filename, 'wb') as f:
                    f.write(view.image)
            except:
                pass

if __name__ == '__main__':
    # Grab credentials from env file
    tokenName, tokenSecret, serverurl, sitename = getCredentials('.env')

    tableau_auth = TSC.PersonalAccessTokenAuth(tokenName, tokenSecret, sitename)
    server = TSC.Server(serverurl)

    # Sign into server
    with server.auth.sign_in(tableau_auth):
        server.use_server_version()
        main()