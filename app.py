import streamlit as st
import numpy as np
import pandas as pd
import json
import time
from collections import OrderedDict
from operator import itemgetter 
    
from functions import *

st.set_page_config(page_title="Pass Net WC18",page_icon="index.png")

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

#Order compositions by alphabetic order
compositions.sort(key=lambda x: x["team"]["name"])

# Creation of dataframe
# change location of the away team (125, 90)
df = get_df(events, compositions[1]["team"]["name"])

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

# Sort TEAM to have the same order
TEAM.sort()

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
    # print(positions)
    positions = plot_avg_map(positions, ax, color="green")
    plot_circuits(df_team_pass, home, positions, ax)
else:
    positions = get_team_avg(df_team_pass, away)
    positions = plot_avg_map(positions, ax, color="red")
    plot_circuits(df_team_pass, away, positions, ax)

st.pyplot(fig)

##### Composition #####
if st.checkbox("Show composition"):
    if team == TEAM[0]:
        st.text(show_composition(home))
    else:
        st.text(show_composition(away))

##### Histogram #####
st.header("Types of pass")
st.pyplot(display_hist(df))


##### Average positions #####
st.header("Average positions")

avg_fig, avg_ax = create_pitch()

df_team1 = get_height_df(df_team, "All")
df_team2 = get_height_df(df_team, "All")

# Home Team
positions1 = get_team_avg(df_team1, home)
positions1 = plot_avg_map(positions1, avg_ax, color="green")

# Away team
positions2 = get_team_avg(df_team2, away)
positions2 = plot_avg_map(positions2, avg_ax, color="red")

print(positions2)

plot_avg_map(positions1, avg_ax)
plot_avg_map(positions2, avg_ax)

st.pyplot(avg_fig)


##### Contact #####
expander = st.beta_expander("Contact")
expander.write("Email : quentinsinh@gmail.com")
expander.write("Github : https://github.com/Qilowa/soccer-visualisation")