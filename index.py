#%% import

import pandas as pd
import streamlit as st
import numpy as np
import requests
import datetime
from tqdm import tqdm
import json
import re

#%% get data

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
text = [x['fullText'] for x in papers]

df = pd.DataFrame({'title':titles,
                   'url':links,
                   'text':abstracts})

# df.to_json(f'core-{datetime.date.today()}.json')

#%%

df = pd.read_json('core-2023-11-25.json')

#%%

# df['text'][:10]

methods = [re.search('Method[\S \n]*Result',x) for x in df['text']]

methods
#%%

for i,method in enumerate(methods):
    if method==None:
        text = df['text'][i]
        l = len(text)
        methods[i] = text[round(l*.15):round(l*.65)]
    else:
        methods[i] = methods[i][0]

methods

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
