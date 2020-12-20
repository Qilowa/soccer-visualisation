import matplotlib.pyplot as plt
import json
import pandas as pd
import os

FILE = "7298.json"

lineup_path = os.path.join("open-data\\data\\lineups", FILE)
events_path = os.path.join("open-data\\data\\events", FILE)

with open(events_path) as json_file:
    events = json.load(json_file)

with open(lineup_path) as json_file:
    lineup = json.load(json_file)

for elem in lineup:
    print(elem["team_name"])
