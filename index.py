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

df = pd.read_json('core-tutors-clean-2023-12-05.json')

df = df.loc[df['readability']<30]

#%% functions for text processing

def md_link(x):
    punc = '\\'.join(string.punctuation)
    no_punc = re.sub(f"[{punc}]",'',x.lower())
    words = re.split(r' +',no_punc)
    return f'#{"-".join(words)}'

def title_case(s):
    return f'{s[0]}{s[1:].lower()}'

with open('text.txt') as f:
    intro = f.read()
    intro = re.sub('\n','\n> ',intro)
    intro = f'> {intro}'

#%% streamlit app

st.markdown('# Living literature review')

page_title = 'Effectiveness of tutoring'

#%% sidebar section

st.sidebar.markdown(f'[{page_title}]({md_link(page_title)})')

for i,row in df.iterrows():
    title = title_case(row["title"])
    st.sidebar.markdown(f'[{" ".join(title.split(" ")[:5])}...]({md_link(title)})')

#%% main section

main, extra = st.columns([.7,.3])

main.markdown(f'## {page_title}')

main.markdown(intro)

main.markdown('This app attempts to do the following:')

main.markdown("""
1. Every month, get the top 10 newest, most cited papers in student achievement from CORE API. 

2. Read in files and using `re` or LLM API, find the main variables, methods, populations, findings of the paper. (Try the Cochrane meta analysis standards as a guide.) 

3. Ideally, these would sit in a repository until a human is able to review (human in the loop design). 

4. Open source - live document that is updated frequently by many experts (GitHub Pages). Users can leave feedback directly on the project. Change log to record version history over time.

5. accessible - language is analyzed for legibility to non-expert audiences (`py-readability-metrics`).

6. Multimodal - includes images, diagrams, videos, and other graphical elements to explain a process visually. 

7. Reproducible - describes methods for meta-analysis that can be applied repeatedly and systematically as new information comes out.

8. Efficient data centralization - instead of several different meta-analyses by individual groups, the *same article will be updated at the same web address over time*, with different sections describing different approaches as needed.

9. Trustworthy - retain the credibility of journals, eg by requiring peer review of each new article/edition (via branches/GitHub).

10. Audience adaptability - show or hide sections or label on a "need-to-know" basis. Outline in left sidebar.
""")

for i,row in df.iterrows():
    main.markdown(f'### {title_case(row["title"])}')
    display = row['display']
    if row['readability']>30:
        display = f'**{display}**'
    main.markdown(display)

#%% optional third panel 

extra.markdown('')
