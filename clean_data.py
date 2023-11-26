"""
Author: Karen Yi
Updated: 11/2023

Process pre-gathered data 

"""

#%% import

import pandas as pd
import re
import numpy as np
import datetime

#%% read data

df = pd.read_json('core-tutors-2023-11-26.json')

# get paper-length papers
df['len'] = [len(x) if not x==None else 0 for x in df['text']]
df = df.loc[df['len']>20000]

df = df.reset_index()

#%% extract methods and results from full text

# df['text_clean'] = [x]

# methods = df['text'][:20]

def truncate(text,start=.15,end=.8):
     return text[round(len(text)*start):round(len(text)*end)]

# remove table of contents
methods = [re.sub('[TABLEOFCONTENTStableofcontents ]{17}.*[\. …]{5,}','',x) for x in df['text']]

# cut as much of intro and references as possible
methods = [truncate(t) for t in methods ]

methods = [re.search('(Method|Research method)[\S \n]+(Discussion|Conclusion)',x) for x in methods]

methods[:10]

#%% 

alternate = '(Design|and method)[\S \n]+(Discussion|Conclusion)'
run_length = 100000

for i,method in enumerate(methods[:run_length]):
    text = df['text'][i]

    # try alternate names for methods section
    if method==None and re.search(alternate,text):
        print(text)
        print(methods[i])
        print(re.search(alternate,text))
        print('\n')
        # print('found it')
        # methods[i] = re.search('Design|method[\S \n]+Result',text)[0]
        
    # last resort, truncate the ~Introduction and ~Discussion, References sections
    if method==None:
        l = len(text)
        methods[i] = text

    # otherwise, use the match from round 1
    else:
        methods[i] = methods[i][0]

methods[:10]

#%% save data

df['methods'] = methods

df[['title','methods']].to_json(f'core-tutors-clean-{datetime.date.today()}.json')

#%% get text from response

def chunk(lst,n):
    """
    Yield n-sized chunks from a list

    https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    """

    for i in range(0,len(lst),n):
        yield lst[i:i+n]

# for i,chunk in enumerate(papers['results']):
#     if i<100:
#         print(chunk.get('fullText'))
#         if chunk.get('fullText'):
#             print(chunk.keys())
#     else:
#         break