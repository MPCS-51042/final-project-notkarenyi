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

#%% get rid of everything before abstract and after references

# remove table of contents
df['text_clean'] = [re.sub('^[A-Z][\S ]+([\.…] *){10,}\d+','',x) for x in df['text']]

# remove everything before abstract (any titles, acknowledgments)
df['text_clean'] = [re.sub('^[\S \n]*(Abstract|ABSTRACT)','Abstract',x) for x in df['text_clean']]

# remove everything after references
df['text_clean'] = [re.sub('(References|REFERENCES)[\S \n]*$','References',x) for x in df['text_clean']]

# remove table of contents again if it didn't work the first time
# for 

# df['text_clean'] = [len(re.findall('\d',x))/len(x) for x in df['results']]

print(df['text_clean'][:10])

print([len(x) for x in df['text_clean'][:10]])

# methods = df['text'][:20]

#%% extract methods and results from full text

def truncate(text,start=.15,end=.8):
    return text[round(len(text)*start):round(len(text)*end)]

def find_section(df, primary='',secondary='',run_length=100000):
    
    # does the first pass work?
    methods = [re.search(primary,x) for x in df['text_clean']]

    for i,method in enumerate(methods):
        text = df['text_clean'][i]

        # try alternate names for methods section
        if method==None and re.search(secondary,text):
            print(text)
            print(methods[i])
            print(re.search(secondary,text))
            print('\n')
            # methods[i] = re.search('Design|method[\S \n]+Result',text)[0]
            
        # last resort, truncate the ~Introduction and ~Discussion, References sections
        if method==None:
            methods[i] = truncate(text,.05,.8)

        # otherwise, use the match from round 1
        else:
            methods[i] = methods[i][0]

    return methods

df['methods_results'] = find_section(df, 
                             primary='(Method|Research method).*(Discussion|Conclusion)',
                             secondary='(Design|and method).*(Discussion|Conclusion)')

print(df['methods_results'][:10])

# (.{10,50}\d+){5,}

#%%

df['methods'] = [re.search('^.*(Result|Analysis)',x) for x in df['methods_results']]
df['methods'] = [x[0] if not x==None else 'NA' for x in df['methods']]

print(df['methods'][:10])

df['results'] = [re.search('(Result|Analysis).*$',x) for x in df['methods_results']]
df['results'] = [x[0] if not x==None else 'NA' for x in df['results']]

print(df['results'][:10])

#%% get conclusion

df['conclusion'] = [re.search('(Conclusion).*$',x) for x in df['text_clean']]
df['conclusion'] = [x[0] if not x==None else 'NA' for x in df['conclusion']]

print(df['conclusion'][:10])

#%% sentence-level TF IDF

from nltk.tokenize import regexp_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def stfidf(text):
    """
    source: https://medium.com/@ashins1997/text-summarization-f2542bc6a167
    """

    sentences = sent_tokenize(text)
    tfidf = TfidfVectorizer()
    result = tfidf.fit_transform(sentences)

    wtfidf = {}
    for word,score in zip(tfidf.get_feature_names_out(), tfidf.idf_):
        wtfidf[word] = score

    # print(wtfidf)
    print(text)

    stfidf = {}
    cv = CountVectorizer()

    for s in sentences:
        # words = word_tokenize(s,r'\w{2,}')
        # words = [w.lower() for w in words if (not w.lower() in stop_words and w.isalpha())]
    
        if len(s)>10:
            try: 
                result = cv.fit_transform([s])
                words = cv.get_feature_names_out()
                stfidf[s] = sum([wtfidf[x] for x in words])
            except Exception as e:
                print(s)
                print(wtfidf.keys())
                print(words)
                print(e)
                stfidf[s] = 0
                continue

    return stfidf

# create column where each entry is a stfidf dict mapping sentences to importance scores
sentence_tfidf = [stfidf(x) for x in df['conclusion']]

sentence_tfidf

#%% sort sentences by importance

# source: https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

threshold = .8

# only get most important sentences
df['display'] = [[k for k,v in x.items() if v>(max(x.values())*threshold)] for x in sentence_tfidf]

#%%

# df['p_digits'] = [len(re.findall('\d',x))/len(x) for x in df['results']]

# print(df['p_digits'][:10])

#%% topic modeling/clustering

# from bertopic import BERTopic

#%%

# import requests
# import json

# url = "https://projects.laion.ai/api/v1/tasks/"

# payload = json.dumps({
#   "type": "summarize_story",
#   "user": {
#     "id": "687886868099891222",
#     "display_name": "notkarenyi",
#     "auth_method": "discord"
#   },
#   "collective": False,
#   "lang": "en"
# })

# headers = {
#   'Content-Type': 'application/json',
#   'Accept': 'application/json'
# }

# response = requests.request("POST", 
#                             url, headers=headers,
#                             data=payload)

# print(response.text)

#%% save data

df[['title','abstract','display']].to_json(f'core-tutors-clean-{datetime.date.today()}.json')

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