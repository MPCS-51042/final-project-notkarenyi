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

#%% clean titles

# remove extra spaces
df['title'] = [re.sub(' {2,}|\n','',x) for x in df['title']]

#%% preprocessing text by truncating as much as possible

def construct_re(start, end, mid='.'):
    # use given and uppercase variants of a regular expression
    return f'({start}|{start.upper()}){mid}*({end}|{end.upper()})'

# remove table of contents
df['text_clean'] = [re.sub('^[A-Z][\S ]+([\.…] *){10,}\d+','',x) for x in df['text']]
df['text_clean'] = [re.sub(construct_re('Table of contents|Table of Contents','(\. ?){3,}|…'),'',x) for x in df['text_clean']]

print(len(df['text_clean'][23]))

# remove everything before abstract (any titles, acknowledgments)
df['text_clean'] = [re.sub(construct_re('^','Abstract',mid='[\S \n]'),'',x) for x in df['text_clean']]

print(len(df['text_clean'][23]))

# remove everything after references or acknowledgments
df['text_clean'] = [x[:10000] + re.sub(construct_re('(References|Acknowledgements)','$',mid='[\S \n]'),'\1',x[10000:]) for x in df['text_clean']]

print(len(df['text_clean'][23]))

# remove table of contents again if it didn't work the first time
# df['text_clean'] = [len(re.findall('\d',x))/len(x) for x in df['results']]

print(df['text_clean'][:10])
print([len(x) for x in df['text_clean']])

# methods = df['text'][:20]

#%% extract methods and results from full text

def truncate(text,start=.15,end=.8):
    # cut off text at start and end percentages
    return text[round(len(text)*start):round(len(text)*end)]

def find_section(docs, start='', end='', start_p=.05, end_p=.95):
    """
    Separate a specific section of text out of a document for each document
    in a corpus

    Note that re.match OR operators evaluate in order: 
    https://stackoverflow.com/questions/35606426/order-of-regular-expression-operator
    
    Params:
        docs (list): 
            corpus of string documents
        start (str): 
            start of search regex, usually a heading
        end (str):
            end of search regex, usually a heading
        start_p (int): 
            beginning percentage at which text should be truncated as last resort
        end_p (int): 
            ending percentage at which text should be truncated as last resort
    """
    
    search = construct_re(start,end)
    search_results = [re.search(search,x) for x in docs]

    # last resort, locate section by approximate location in document
    section = [truncate(docs[i],start_p,end_p) if result==None else result[0] for i,result in enumerate(search_results)]

    return section

# note that text_clean is already stripped of TOC, abstract, and references

df['methods'] = find_section(df['text_clean'], 
                             start='Method|Research method|Design|and method',
                             end='Result|Analysis',
                             start_p=.2,
                             end_p=.6)
print(df['methods'][:10])

df['results'] = find_section(df['text_clean'], 
                             start='Result|Analysis', 
                             end='Discussion|Conclusion',
                             start_p=.5,
                             end_p=.8)
print(df['results'][:10])

df['conclusion'] = find_section(df['text_clean'], 
                             start='Discussion|Conclusion', 
                             end='$',
                             start_p=.7,
                             end_p=1)
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
        (dict): mapping sentences to importance scores

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
        if len(s)>30:
            try: 
                result = cv.fit_transform([s])
                words = cv.get_feature_names_out()
                # sum the importance of each sentence via the word level TFIDF
                stfidf[s] = sum([wtfidf[x] for x in words])
            except Exception as e:
                # catch and examine errors
                print(s)
                # print(wtfidf.keys())
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

# flatten into string
df['display'] = [re.sub('(\.\.\. ){2,}','', ' '.join(x)) for x in df['display']]

#%% readability scoring

from readability import Readability

df = df.loc[[len(x.split(' '))>100 for x in df['display']]]

df['readability'] = [Readability(x).flesch_kincaid().grade_level for x in df['display']]

#%% save data

df[['title','abstract','display','readability']].to_json(f'core-tutors-clean-{datetime.date.today()}.json')
