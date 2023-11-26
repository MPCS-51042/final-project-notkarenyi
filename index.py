#%% import

import pandas as pd
import streamlit as st
import numpy as np
import requests
# from pyalex import Works
import datetime
# from crossref.restful import Works, Etiquette
from tqdm import tqdm
import json

#%% setup

# pyalex.config.email = "notkarenyi@gmail.com"

# my_etiquette = Etiquette('MPCS Final Project', 'v0', 'https://github.com/MPCS-51042/final-project-notkarenyi', 'karenyi@uchicago.edu')

# works = Works(etiquette=my_etiquette)
   
params = {
    # semantic scholar
    # 'x-api-key':'1lYvegdgMq1ON1bVdEblh6hk98s7Ta7J3vt0wIKR',
    # 'query':'high-school student achievement policy',
    # 'publicationDateOrYear':f'{date.today().year}-{date.today().month}'

    # springer
    # 'api_key':
    # 'q': 'high-school student achievement policy'
}

#%% get data

# response = requests.get('http://api.semanticscholar.org/graph/v1/paper/search?',params=params)

# response = requests.get('http://api.springernature.com/openaccess',params=params)

# response = works.query(bibliographic='education achievement policy').filter(from_created_date=date(2023,11,1),has_full_text='true',type='journal-article')

# print(response.count())

def query_api(endpoint, query, limit=100, is_scroll=False, scrollId=None):
    """
    Query CORE API for papers matching a query

    Params:
        endpoint (str):
            URL endpoint to specify
        query (str):
            Google-like query to search for relevant papers
        limit (int):
            Max of 100, how many papers to return?
        is_scroll (bool):
            Are we scrolling?
        scrollId (int):
            Scroll position

    Return:
        json (dict-like) of API response (access ['results'] for results)
        time elapsed (seconds)
    
    Source: 
        https://github.com/oacore/apiv3-webinar/blob/main/webinar.ipynb
    """

    headers={"Authorization":"Bearer "+'BhtARGyaxXQ0INUjqKc5LSVprPCiuYFT'}
    
    query = {"q":query, "limit":limit}

    # scrolling through results max 100 at a time
    if not scrollId:
        query["scroll"]="true"
    elif is_scroll:
        query["scrollId"]=scrollId

    # API call
    response = requests.post(f'https://api.core.ac.uk/v3/{endpoint}',data = json.dumps(query), headers=headers)

    if response.status_code ==200:
        return response.json(), response.elapsed.total_seconds()
    else:
        print(f"Error code {response.status_code}, {response.content}")

def scroll(endpoint, query, extract_info_callback=None):
    """
    Query CORE API, while scrolling through results.

    Params:
        endpoint (str):
            URL endpoint to specify
        query (str):
            Google-like query to search for relevant papers

    Source:
        https://github.com/oacore/apiv3-webinar/blob/main/webinar.ipynb
    """

    allresults = []
    count = 0
    scrollId=None
    while True:
        result, elapsed =query_api(endpoint, query, is_scroll=True, scrollId=scrollId)
        scrollId=result["scrollId"]
        totalhits = result["totalHits"]
        result_size = len(result["results"])
        if result_size==0:
            break
        for hit in result["results"]:
            if extract_info_callback:
              allresults.append(extract_info_callback(hit))
            else:
              allresults.append(hit)
        count+=result_size
        print(f"{count}/{totalhits} {elapsed}s")
    return allresults


day = datetime.date.today() - datetime.timedelta(weeks=1)
papers = scroll("search/works",f'high-school student achievement policy AND createdDate>={day}')
# print(papers['results'])

#%%

titles = [x['title'] for x in papers]
links = [x.get('url') for x in papers]
abstracts = [x['fullText'] for x in papers]

df = pd.DataFrame({'title':titles,
                   'url':links,
                   'abstract':abstracts})

df.to_json('core-112523.json')

#%% get text from response

def chunk(lst,n):
    """
    Yield n-sized chunks from a list

    https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    """

    for i in range(0,len(lst),n):
        yield lst[i:i+n]

for i,chunk in enumerate(papers['results']):
    if i<100:
        print(chunk.get('fullText'))
        if chunk.get('fullText'):
            print(chunk.keys())
    else:
        break

#%% streamlit app

st.markdown('# Living literature review')

st.sidebar.markdown('[Effective ways to increase high-school student achievement](#effective-ways-to-increase-high-school-student-achievement)')

main, extra = st.columns([.7,.3])

main.markdown('## Effective ways to increase high-school student achievement')

main.markdown('\n\n\n\n\n\n\n\n\n\nsdfsdf')

extra.markdown('Here is extra content')
