"""
Author: Karen Yi
Updated: 11/2023

Run a streamlit app.
"""
#%% import

import pandas as pd
import streamlit as st
import string
from nltk.tokenize import word_tokenize
import re

#%% import data

df = pd.read_json('core-tutors-clean-2023-12-03.json')

#%% 

def md_link(x):
    punc = '\\'.join(string.punctuation)
    no_punc = re.sub(f"[{punc}]",'',x.lower())
    words = re.split(r' +',no_punc)
    return f'#{"-".join(words)}'

def title_case(s):
    return f'{s[0]}{s[1:].lower()}'

#%% streamlit app

st.markdown('# Living literature review')

page_title = 'Effectiveness of tutoring'

# sidebar section

st.sidebar.markdown(f'[{page_title}]({md_link(page_title)})')

for i,row in df.iterrows():
    title = title_case(row["title"])
    st.sidebar.markdown(f'[{" ".join(title.split(" ")[:5])}...]({md_link(title)})')

# main section

main, extra = st.columns([.7,.3])

main.markdown(f'## {page_title}')

main.markdown('This app attempts to do the following:')

for i,row in df.iterrows():
    main.markdown(f'### {title_case(row["title"])}')
    display = re.sub('(\.\.\. ){2,}',
                     '',
                     ' '.join(row['display']))
    main.markdown(display)

extra.markdown('Here is extra content')
