import streamlit as st
import numpy as np
import pandas as pd
import json
import time
    
from functions import *

PATH = os.path.join("worldcup", "7556.json")

    
st.title('My first app')

st.write("Here's our first attempt at using data to create a table:")

compositions, events = get_comp_events(PATH)

df = get_df(events)

home, away = get_formations(compositions)

fig, ax = create_pitch()
positions = get_team_avg(df, home)
positions = plot_avg_map(positions, ax)
plot_circuits(df, home, positions, ax)

st.pyplot(fig)

if st.checkbox('Show dataframe'):
    st.write(df.head())


option = st.sidebar.selectbox(
    'Which number do you like best?',
     df['minute'])

'You selected:', option

