"""
Author: Karen Yi
Updated: 11/2023

Process pre-gathered data 

"""

#%% import

import pandas as pd
import re
import numpy as np

#%% read data

df = pd.read_json('core-tutors-2023-11-25.json')

# get paper-length papers
df = df.loc[[len(x)>5000 for x in df['text']]]

df = df.reset_index()

#%% extract methods from full text

# df['text_clean'] = [x]

# methods = df['text'][:20]

# remove table of contents
methods = [re.sub('[TABLEOFCONTENTStableofcontents ]{17}.*[\. …]{5,}','',x) for x in df['text']]

methods = [re.search('(Design|Method)[\S \n]+Result',x) for x in methods]

methods

#%%

for i,method in enumerate(methods):
    text = df['text'][i]
    if method==None:
        l = len(text)
        methods[i] = text[round(l*.15):round(l*.65)]
    elif re.search('method[\S \n]+Result',text):
        # print('found it')
        methods[i] = re.search('method[\S \n]+Result',text)
    else:
        methods[i] = methods[i][0]

methods

#%%

df['methods'] = methods

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