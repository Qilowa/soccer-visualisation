import streamlit as st
import numpy as np
import pandas as pd
import json
import time
    
from functions import *

DIR = "worldcup"

FILES = []

for f in os.listdir(DIR):
    if f[0] == "7":
        FILES.append(f)

file = st.sidebar.select_slider(
    "Select file",
    options=FILES
)

PATH = os.path.join(DIR, file)

# Get data
compositions, events = get_comp_events(PATH) 

# Creation of dataframe
df = get_df(events)

# Getting informations on teams
home, away = get_formations(compositions)

# Set title
st.title(f'{home["team"]} vs {away["team"]} 2018 World Cup')

##### Description #####
st.header("Description")
st.write("Here's a little app displaying the passing network of matches during the 2018 World Cup")

##### PASSING NETWORK #####
st.header("Passing Network :sunglasses:")

# Create pitch
fig, ax = create_pitch() 

passes = get_pass_df(df)

PASS_HEIGHT = list(passes.height_pass.unique()) + ["All"]
TEAM = list(passes.team.unique())

height_pass = st.sidebar.radio(
    "What type of pass",
    PASS_HEIGHT
)

team = st.sidebar.radio(
    "What team",
    TEAM
)

df_team = get_team_df(passes, team) # get team

df_team_pass = get_height_df(df_team, height_pass) # get type of pass

if team == TEAM[0]:
    positions = get_team_avg(df_team_pass, home)
    positions = plot_avg_map(positions, ax, color="green")
    plot_circuits(df_team_pass, home, positions, ax)
else:
    positions = get_team_avg(df_team_pass, away)
    positions = plot_avg_map(positions, ax, color="red")
    plot_circuits(df_team_pass, away, positions, ax)
st.pyplot(fig)

##### Histogram #####
st.header("Type of pass per team")
st.pyplot(display_hist(df))


##### Composition #####
if st.checkbox("Show composition"):
    if team == TEAM[0]:
        st.text(show_composition(home))
    else:
        st.text(show_composition(away))


##### Contact #####
expander = st.beta_expander("Contact")
expander.write("Email : quentinsinh@gmail.com")