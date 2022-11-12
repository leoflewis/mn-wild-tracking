import hockey_scraper, pandas

# This program constructs a data set for Expected Goals model.
# We want Fenwick(unblocked) shot data for as many games as possible. 

# Scrape data
print("Begining to scrape pbp. No shifts. Depening on what timerange was requested, this could take awhile.")
data = hockey_scraper.scrape_games([2022020210], False, data_format='Pandas')
print("Finished scraping.")

# Access dataframe
df = data['pbp']
print(df.columns)

# Drop unnecessary columns
df.drop(['Game_Id', 'Date', 'Description', 'Time_Elapsed',
       'Seconds_Elapsed', 'Strength', 'Ev_Zone', 'Ev_Team',
        'Away_Team', 'Home_Team', 'p1_ID', 'p2_name',
       'p2_ID', 'p3_name', 'p3_ID', 'awayPlayer1', 'awayPlayer1_id',
       'awayPlayer2', 'awayPlayer2_id', 'awayPlayer3', 'awayPlayer3_id',
       'awayPlayer4', 'awayPlayer4_id', 'awayPlayer5', 'awayPlayer5_id',
       'awayPlayer6', 'awayPlayer6_id', 'homePlayer1', 'homePlayer1_id',
       'homePlayer2', 'homePlayer2_id', 'homePlayer3', 'homePlayer3_id',
       'homePlayer4', 'homePlayer4_id', 'homePlayer5', 'homePlayer5_id',
       'homePlayer6', 'homePlayer6_id', 'Away_Players', 'Home_Players',
       'Away_Score', 'Home_Score', 'Away_Goalie_Id',
       'Home_Goalie_Id', 'Home_Coach',
       'Away_Coach'], axis=1, inplace=True)

print(df.columns)
print(df.head)

# Drop empty values, this will get rid of lots of unecessary events. It will also get rid of empty net goals.
df.dropna(inplace=True)
print(df.head)

# Drop worthless events
events = df[ (df.Event == 'FAC') | (df.Event == 'BLOCK') | (df.Event == 'PENL') | (df.Event == 'GIVE') | (df.Event == 'TAKE') | (df.Event == 'STOP') | (df.Event == 'HIT')].index
df.drop(events, inplace=True)


# We need to transpose goals/shots/misses so it reads as if they all happen on the same net.
df.loc[(df['Period'].eq(1) | df['Period'].eq(3)) & df['Home_Zone'].eq('Def'), 'xC'] = df['xC'] * -1
df.loc[(df['Period'].eq(1) | df['Period'].eq(3)) & df['Home_Zone'].eq('Def'), 'yC'] = df['yC'] * -1

df.loc[(df['Period'].eq(2) | df['Period'].eq(4)) & df['Home_Zone'].eq('Off'), 'xC'] = df['xC'] * -1
df.loc[(df['Period'].eq(2) | df['Period'].eq(4)) & df['Home_Zone'].eq('Off'), 'yC'] = df['yC'] * -1

# Next we need to add a column for distance to net.
