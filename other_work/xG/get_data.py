import hockey_scraper, pandas, numpy, math
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from joblib import dump

# This program constructs a data set and an Expected Goals model.

# We want Fenwick(unblocked) shot data for as many games as possible. 

# Scrape data
print("Begining to scrape pbp. No shifts. Depending on what timerange was requested, this could take awhile.")
data = hockey_scraper.scrape_seasons([2021], False, data_format = 'Pandas')
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
       'Away_Coach', 'Home_Zone', 'p1_name'], axis=1, inplace=True)


# Drop empty values, this will get rid of lots of unecessary events. It will also get rid of empty net goals.
df.dropna(inplace=True)


# Drop worthless events, also drop shootout events
events = df[ (df.Event == 'FAC') | (df.Event == 'BLOCK') | 
    (df.Event == 'PENL') | (df.Event == 'GIVE') | (df.Event == 'TAKE') | 
    (df.Event == 'STOP') | (df.Event == 'HIT') | (df.Period == 5)].index

df.drop(events, inplace=True)

# Add a binary column for Goals 
df['Goal'] = numpy.where(df.Event == 'GOAL', 1, 0)

df.drop(['Away_Goalie', 'Home_Goalie', 'Event', 'Strength'], axis=1, inplace=True)

# We need to transpose goals/shots/misses so it reads as if they all happen on the same net.
# So we will tranpose the shot location if it is in the negative half of the rink.
# Technically this could incorrecly move some shots that occur form over the red line.
# Those dont happen very often and we already removed empty net goals, so there shouldnt be any goals from beyond the red line.
# This will add a couple shots that take place behind the net, but they will never be goals, so it wont give them a good score.
# Overall this could add a little extra noise, but it should not be anything too serious. 
df.loc[(df['xC'] < 0), 'yC'] = df['yC'] * -1
df.loc[(df['xC'] < 0), 'xC'] = df['xC'] * -1

# This function calculates the angle to the center of the net at (89, 0) in radians and degrees.
def angles(x, y):
    num = math.sqrt(((89.0 - x) * (89.0 - x)) + ((y) * (y)))
    radians = numpy.arcsin(y/num)
    degrees = (radians * 180.0) / 3.14
    arr = [radians, degrees]
    return arr


# We will employ one categorical variable, the shot type.
# The get_dummies function will create columns for a binary labeling of all 8 of the shot types. 
df = pandas.get_dummies(df)

# Initiliaze empty columns
df['Angle_Radians'] = ''
df['Angle_Degrees'] = ''
df['Distance'] = ''

# Add values to columns
# If someone wants to show me a quicker way to do this, I would be very greatful.  
for index, row in df.iterrows():
    x = row['xC']
    y = row['yC']
    all_angles = angles(x, y)
    df.at[index, 'Angle_Radians'] = all_angles[0]
    df.at[index, 'Angle_Degrees'] = all_angles[1]
    df.at[index, 'Distance'] = numpy.sqrt((y - 0)**2 + (x - 89.0)**2)

with pandas.option_context('display.max_rows', 1000,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df)

print(df['Distance'].mean())

# Data should be good to go at this point. 
# We will build the model
predictors = ['xC', 'yC', 'Type_', 'Type_BACKHAND', 'Type_DEFLECTED', 'Type_SLAP SHOT', 'Type_SNAP SHOT', 'Type_TIP-IN', 'Type_WRAP-AROUND', 'Type_WRIST SHOT', 'Angle_Radians', 'Angle_Degrees', 'Distance']
x = df[predictors]
y = df.Goal
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size =.2, random_state=16)
model = LogisticRegression()
model.fit(x_train, y_train)
score = model.score(x_test, y_test)
predictions = model.predict(x_test)
print(score)
cm = metrics.confusion_matrix(y_test, predictions)
print("confusion matrix: ")
print(cm)
print("coefficients: "+ str(model.coef_))

# Our columns after modeling are as follows:
# Period, xC, yC, Goal, Type_, Type_BACKHAND, Type_DEFLECTED, Type_SLAP SHOT, Type_SNAP SHOT, Type_TIP-IN, Type_WRAP-AROUND, Type_WRIST SHOT, Angle_Radians, Angle_Degrees, Distance


# Lets make a prediction
x = 86
y = -6
new_angles = angles(x, y)
new_distance = numpy.sqrt((y - 0)**2 + (x - 89.0)**2)
new_shot = [[x, y, 0, 0, 0, 1, 0, 0, 0, 0, new_angles[0], new_angles[1], new_distance]]
new_df = pandas.DataFrame(new_shot, columns=predictors)
pred = model.predict_proba(new_df) 
print("odds of 0 and 1: " + str(pred))


# Adding another point with -1 goal value that serve as the net in the graph created below
df.loc[len(df.index)] = [0, 89, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sns.scatterplot(x='xC', y='yC', hue='Goal', marker='o', data=df)
plt.savefig("xG.png")
dump(model, 'xG.joblib')