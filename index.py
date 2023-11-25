#%%

import pandas as pd
import streamlit as st
import numpy as np
import requests
# from pyalex import Works
from datetime import date
from crossref.restful import Works, Etiquette
from tqdm import tqdm
import json

#%%

# pyalex.config.email = "notkarenyi@gmail.com"

my_etiquette = Etiquette('MPCS Final Project', 'v0', 'https://github.com/MPCS-51042/final-project-notkarenyi', 'karenyi@uchicago.edu')
   
params = {
    # semantic scholar
    # 'x-api-key':'1lYvegdgMq1ON1bVdEblh6hk98s7Ta7J3vt0wIKR',
    # 'query':'high-school student achievement policy',
    # 'publicationDateOrYear':f'{date.today().year}-{date.today().month}'

    # springer
    # 'api_key':
    # 'q': 'high-school student achievement policy'
    
    # core
    'api_key': ''
}

# response = requests.get('http://api.semanticscholar.org/graph/v1/paper/search?',params=params)

# works = Works(etiquette=my_etiquette)

# response = requests.get('http://api.springernature.com/openaccess',params=params)


def query_api(url_fragment, query,limit=100):
    headers={"Authorization":"Bearer "+'BhtARGyaxXQ0INUjqKc5LSVprPCiuYFT'}
    
    query = {"q":query, "limit":limit}

    response = requests.post(f'https://api.core.ac.uk/v3/{url_fragment}',data = json.dumps(query), headers=headers)

    if response.status_code == 200:
        return response.json(), response.elapsed.total_seconds()
    else:
        print(f"Error code {response.status_code}, {response.content}")

data_provider, elapsed = query_api("search/data-providers")
print(json.dumps(data_provider),indent=2)

#%%

# response = works.query(bibliographic='education achievement policy').filter(from_created_date=date(2023,11,1),has_full_text='true',type='journal-article')

print(response.count())

#%%

def chunk(lst,n):
    """
    Yield n-sized chunks from a list

    https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    """

    for i in range(0,len(lst),n):
        yield lst[i:i+n]

for i,chunk in enumerate(response):
    if i<5:
        print(chunk.get('abstract'))
        if chunk.get('abstract'):
            print(chunk.keys())
    else:
        break

#%%

for i in response:
    print(i)

#%% streamlit app

st.markdown('# Living literature review')

st.sidebar.markdown('[Effective ways to increase high-school student achievement](#effective-ways-to-increase-high-school-student-achievement)')

main, extra = st.columns([.7,.3])

main.markdown('## Effective ways to increase high-school student achievement')

main.markdown('\n\n\n\n\n\n\n\n\n\nsdfsdf')

extra.markdown('Here is extra content')
