import hockey_scraper, pandas

#This program constructs a data set for Expected Goals model.

#scrape data
print("Begining to scrape pbp. No shifts.")
data = hockey_scraper.scrape_games([2022020210], False, data_format='Pandas')
print("Finished scraping.")

#access dataframe
df = data['pbp']
print(df.columns)

#drop unnecessary columns
df.drop(['Game_Id', 'Date', 'Description', 'Time_Elapsed',
       'Seconds_Elapsed', 'Strength', 'Ev_Zone', 'Ev_Team',
        'Away_Team', 'Home_Team', 'p1_name', 'p1_ID', 'p2_name',
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
df.dropna(inplace=True)
print(df.head)