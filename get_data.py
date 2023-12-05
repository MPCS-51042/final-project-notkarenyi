"""
Author: Karen Yi
Updated: 11/2023

Gather full-text data about high-school student achievement from CORE API on a semi annual basis.
"""
#%% import

import pandas as pd
import requests
import datetime
from tqdm import tqdm
import json
import re

#%% functions

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

day = datetime.date.today() - datetime.timedelta(weeks=24)

query = f'(abstract:tutor OR abstract:paraprofessional) AND abstract:student AND createdDate>={day} AND language=English'

#%% test

# papers = query_api("search/works",query,limit=10)

#%% get data

papers = scroll("search/works",query)
# print(papers['results'])

#%% extract relevant info and save

titles = [x['title'] for x in papers]
abstracts = [x['abstract'] for x in papers]
links = [x.get('url') for x in papers]
text = [x['fullText'] for x in papers]

df = pd.DataFrame({'title':titles,
                   'abstract':abstracts,
                   'url':links,
                   'text':text})

df.to_json(f'core-tutors-{datetime.date.today()}.json')
