"""
Author: Karen Yi
Updated: 11/2023

Run a streamlit app.
"""
#%% import

import pandas as pd
import streamlit as st

#%% streamlit app

st.markdown('# Living literature review')

st.sidebar.markdown('[Effective ways to increase high-school student achievement](#effective-ways-to-increase-high-school-student-achievement)')

main, extra = st.columns([.7,.3])

main.markdown('## Effective ways to increase high-school student achievement')

main.markdown('\n\n\n\n\n\n\n\n\n\nsdfsdf')

extra.markdown('Here is extra content')
