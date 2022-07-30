#!/usr/bin/env python3

from datetime import datetime
import requests
from pathlib import Path
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date

def getTablesViews(soup,version):
    tables = pd.read_html(str(soup),header=0)[:2]
    dfs = []
    for df in tables:
        table_type = list(df.columns)[0].split(' ')[0]
        df['TableName'] = table_type + ': list of ' + table_type + 's'
        df.rename(columns={df.columns[0]: 'Name'}, inplace=True)
        df['Version'] = version
        dfs.append(df)
    
    return dfs
    
def getTables(soup,version):
    tables = pd.read_html(str(soup),header=[0,1])[2:]
    dfs = []
    for df in tables:
        table_name = df.columns.levels[0][0]
        df = df.droplevel(0, axis='columns')
        df['TableName'] = table_name
        df['Version'] = version
        df.dropna(inplace=True)
        df.reset_index(inplace=True)
        df['FieldOrder'] = df['index']
        del df['index']
        dfs.append(df)
    
    return dfs

def getData(version):
    url = 'https://tableau.github.io/tableau-data-dictionary/{}/data_dictionary.htm'.format(version)
    # Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    
    if not page:
        return [], []
    
    # Remove all footer rows (Eg. Foreign Key notes)
    soup = BeautifulSoup(page.text, 'html.parser')
    for footer in soup.find_all('tfoot'):
        footer.decompose()

    dfs1 = getTablesViews(soup,version)
    dfs2 = getTables(soup,version)
    return dfs1, dfs2

def addAttributes(name,df):
    df[['TableName', 'TableDescription']] = df['TableName'].str.split(':', n=1, expand=True)
    if name == 'TablesViews':
        df['Name'] = df['Name'].apply(lambda x: x if '.' in x else 'public.' + x)
        df['Identifier'] = df['Name']
    else:
        df['TableName'] = df['TableName'].apply(lambda x: x if '.' in x else 'public.' + x)
        df['Identifier'] = df['TableName'] + df['Name']
        
    df['VersionMin'] = df.groupby(['Identifier'])['Version'].transform(min)
    df['VersionMax'] = df.groupby(['Identifier'])['Version'].transform(max)
    
    # Get current path of script
    filepath = Path(Path(__file__).parent) / 'zzzOutputs'
    filepath.mkdir(exist_ok=True)
    filename = filepath / (name + '.csv')
    df.to_csv(filename, index=False)
    

def main():
    tables_views_df = []
    table_df = []
    current_year = date.today().year
    years = range(2019,current_year+1)
    releases = [1,2,3,4]
    
    for year in years:
        for release in releases:
            version = str(year) + '.' + str(release)
            print('Grabbing {} . . .'.format(version))
            dfs1, dfs2 = getData(version)
            tables_views_df.extend(dfs1)
            table_df.extend(dfs2)
            
    tables_views = pd.concat(tables_views_df)
    tables = pd.concat(table_df)
    
    type_to_df = {
        'TablesViews': tables_views,
        'TableMetadata': tables
    }
    
    for name, df in type_to_df.items():
        addAttributes(name, df)
            
if __name__ == '__main__':
    main()