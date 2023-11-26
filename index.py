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

df = pd.read_json('core-tutors-clean-2023-11-26.json')

#%%

def remove_punc(x):
    return re.sub('\\'.join(string.punctuation),'',x)

#%% streamlit app

st.markdown('# Living literature review')

title = 'Effectiveness of tutoring'

# sidebar section

st.sidebar.markdown(f'[{title}](#{"-".join(title.lower().split(" "))})')

for i,row in df.iterrows():
    st.sidebar.markdown(f'[{row["title"]}](#{"-".join(remove_punc(row["title"]).lower().split(" "))})')

# main section

main, extra = st.columns([.7,.3])

main.markdown(f'## {title}')

main.markdown('\n\n\n\n\n\n\n\n\n\nsdfsdf')

for i,row in df.iterrows():
    main.markdown(f'### {row["title"]}')
    main.markdown(f'{row["methods"][:1000]}')

extra.markdown('Here is extra content')
