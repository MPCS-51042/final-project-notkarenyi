"""
Author: Karen Yi
Updated: 12/2023

Process pre-gathered data using various NLP techniques.

"""

#%% import

import pandas as pd
import re
import numpy as np
import datetime

#%% read data

df = pd.read_json('core-tutors-2023-11-26.json')

# which entries are long enough to be a paper?

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

#%% separate methods and results

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
    Construct a sentence-level TF-IDF where the numerator is related to the number
    of times a word appears in a sentence and the denominator is related to the 
    number of times a word appears in the document overall.

    Higher score 

    Params:
        text (str): document to parse

    Return:


    Source: https://medium.com/@ashins1997/text-summarization-f2542bc6a167
    """

    # separate string into sentences
    sentences = sent_tokenize(text)

    # get word level TDIDF
    tfidf = TfidfVectorizer()
    result = tfidf.fit_transform(sentences)

    # map words to their scores
    wtfidf = {}
    for word,score in zip(tfidf.get_feature_names_out(), tfidf.idf_):
        wtfidf[word] = score

    # print(wtfidf)
    # print(text)

    # initialize sentence-level TFIDF
    stfidf = {}

    # use the same tokenizer as for TFIDF to get the words per sentence
    cv = CountVectorizer()
    for s in sentences:
    
        # if we have a long enough sentence, over 10 chars:
        if len(s)>10:
            try: 
                result = cv.fit_transform([s])
                words = cv.get_feature_names_out()
                # sum the importance of each sentence via the word level TFIDF
                stfidf[s] = sum([wtfidf[x] for x in words])
            except Exception as e:
                # catch and examine errors
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

# get most important sentences
# use ellipsis as placeholder for skipped sentences
df['display'] = [[k if v>(max(x.values())*threshold) else '...' for k,v in x.items()] for x in sentence_tfidf]

#%%

# df['p_digits'] = [len(re.findall('\d',x))/len(x) for x in df['results']]

# print(df['p_digits'][:10])

#%% topic modeling/clustering

# from bertopic import BERTopic

#%% save data

df[['title','abstract','display']].to_json(f'core-tutors-clean-{datetime.date.today()}.json')
