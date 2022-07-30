import json
import pandas as pd
import urllib3

def getResults(start, count, keyword):
    # initalize total hits variable
    # use 100 since this is the max count we can return
    total_hits = 100
    while start < total_hits:
        api_call = "https://public.tableau.com/api/search/query?count={}&language=en-us&query={}&start={}&type=authors".format(count,keyword,start)
        http = urllib3.PoolManager()
        search = json.loads(http.request('GET',api_call).data)
        if start == 0:
            total_hits = search['totalHits']
            print('Retrieving {} Tableau Public Authors!'.format(total_hits))
            search_results = search['results']
        else:
            # append additional json results
            search_results.extend(search['results'])
        start += count

    df = pd.DataFrame(search_results)
    return df

def getAuthors(df):
    # Grab Author portion
    author_df = pd.json_normalize(df['author'])
    # Add URL
    author_df['profileUrl'] = 'https://public.tableau.com/app/profile/' + author_df['profileName']
    # Convert ms timestamps to date
    if 'createdAt' in author_df.columns:
        author_df['createdAt'] = pd.to_datetime(author_df['createdAt'], unit='ms', origin='unix', errors='coerce').dt.date
    if 'lastPublishDate' in author_df.columns:
        author_df['lastPublishDate'] = pd.to_datetime(author_df['lastPublishDate'], unit='ms', errors='coerce').dt.date
    # Convert address dictionary to column
    author_df['address'] = author_df['address'].map(lambda d: {} if pd.isna(d) or not str(d).startswith('{') else json.loads(d))
    
    author_df['country'] = author_df['address'].apply(lambda x: x.get('country', ''))
    author_df['state'] = author_df['address'].apply(lambda x: x.get('state', ''))
    author_df['city'] = author_df['address'].apply(lambda x: x.get('city', ''))
    # Cleanup
    author_df.drop(['workbooks', 'gravatarHash', 'avatarUrl', 'searchable', 'address'], axis=1, inplace=True)
    
    # Export full list
    author_df.to_csv('./PublicAuthors.csv', index=False)
    
    return author_df
    
def filterAuthors(author_df, filter_dict):
    # use dictionary as filter
    filtered_df = author_df.loc[(author_df[list(filter_dict)] == pd.Series(filter_dict)).all(axis=1)]
    print('Saving filtered list of {} authors!'.format(len(filtered_df)))
    filtered_df.to_csv('./PublicAuthorsFiltered.csv', index=False)
    return

def main():
    start = 0
    count = 100
    keyword = 'california'
    df = getResults(start, count, keyword)
    author_df = getAuthors(df)
    # Create dictionary of columns to values
    # This will be used to filter dataframe
    
    # List of columns:
        # bio, city, country, createdAt
        # featuredVizRepoUrl, freelance, lastPublishDate
        # name, organization, profileName, profileUrl
        # state, title, totalNumberOfFollowers, totalNumberOfFollowing
        # visibleWorkbookCount, vizCount
    filter_dict = {'state': 'California', 'freelance': True}
    
    filterAuthors(author_df, filter_dict)
    print('All set!')

if __name__ == '__main__':
    main()