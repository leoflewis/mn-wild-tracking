import hockey_scraper, pandas, numpy, math

# This program constructs a data set and an Expected Goals model.

# We want Fenwick(unblocked) shot data for as many games as possible. 

# Scrape data
print("Begining to scrape pbp. No shifts. Depending on what timerange was requested, this could take awhile.")
data = hockey_scraper.scrape_games([2021020001, 2021020002, 2021020003, 2021020004], False, data_format = 'Pandas')
print("Finished scraping.")

# Access dataframe
df = data['pbp']

# Drop unnecessary columns
df.drop(['Game_Id', 'Date', 'Description', 'Time_Elapsed',
       'Seconds_Elapsed', 'Ev_Zone', 'Ev_Team',
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

# Drop empty values, this will get rid of lots of unecessary events. It will also get rid of empty net goals.
df.dropna(inplace=True)

# Drop worthless events, also drop shootout events
events = df[ (df.Event == 'FAC') | (df.Event == 'BLOCK') | (df.Event == 'PENL') | (df.Event == 'GIVE') | (df.Event == 'TAKE') | (df.Event == 'STOP') | (df.Event == 'HIT') | (df.Period == 5)].index
df.drop(events, inplace=True)

# We need to transpose goals/shots/misses so it reads as if they all happen on the same net.
# So we will tranpose the shot location if it is in the negative half of the rink.
# Technically this could incorrecly move some shots that occur form over the red line.
# Those dont happen very often and we alreay removed empty net goals, so there shouldnt be any goals from beyond the red line.
# Overall this could add a little extra noise, but it should not be anything too serious. 
df.loc[(df['xC'] < 0), 'yC'] = df['yC'] * -1
df.loc[(df['xC'] < 0), 'xC'] = df['xC'] * -1

# Add a binary column for Goals 
df['Goal'] = numpy.where(df.Event == 'GOAL', 1, 0)

# This functions calculate the angle to the center of the net at (87.50, 0) in radians and degrees.
def angles(x, y):
    num = math.sqrt(((89.0 - x) * (89.0 - x)) + ((y) * (y)))
    radians = numpy.arcsin(y/num)
    degrees = (radians * 180.0) / 3.14
    arr = [radians, degrees]
    return arr

# Initiliaze empty columns
df['Angle Radians'] = ''
df['Angle Degrees'] = ''
df['Distance'] = ''

# Add values to columns
# If someone wants to show me a quicker way to do this, I would be very greatful.  
for index, row in df.iterrows():
    x = row['xC']
    y = row['yC']
    all_angles = angles(x, y)
    df.at[index, 'Angle Radians'] = all_angles[0]
    df.at[index, 'Angle Degrees'] = all_angles[1]
    df.at[index, 'Distance'] = numpy.sqrt((y - 0)**2 + (x - 89.0)**2)

with pandas.option_context('display.max_rows', 1000,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df)

print(df['Distance'].mean())