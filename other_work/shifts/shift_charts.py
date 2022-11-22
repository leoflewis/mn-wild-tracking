import requests, matplotlib.pyplot as plt, numpy as np, pandas

def convert_time(time):
    return (int(time[0:2]) + (int(time[3:5]) / 100))

def convert_start_time(time, period):
    period = int(period)
    if period == 2:
        return 20 + (int(time[0:2]) + (int(time[3:5]) / 100))
    if period == 3:
        return 40 + (int(time[0:2]) + (int(time[3:5]) / 100))
    if period == 4:
        return 60 + (int(time[0:2]) + (int(time[3:5]) / 100))
    if period == 6:
        return 100 + (int(time[0:2]) + (int(time[3:5]) / 100))
    return (int(time[0:2]) + (int(time[3:5]) / 100))


id = 2022020283
response = requests.get("https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={}".format(id))
shifts = response.json()['data']

df = pandas.DataFrame(shifts)
df = df.astype(str)
df['name'] = df.firstName + " " + df.lastName

df.drop(['eventDescription', 'detailCode', 'eventDetails', 'typeCode', 'gameId', 'shiftNumber', 'teamName', 'hexValue', 'id', 'eventNumber', 'teamId', 'firstName', 'lastName'], axis=1, inplace=True)
df = df.astype(str)
df['color'] = np.where(df.teamAbbrev == 'MIN', 'b', 'r')

for index, row in df.iterrows():
    period = row['period']

    start_time = row['startTime']
    stime = convert_start_time(start_time, period) 
    df.at[index, 'startTime'] = stime

    end_time = row['endTime']
    etime = convert_start_time(end_time, period) 
    df.at[index, 'endTime'] = etime

    total = etime - stime
    df.at[index, 'duration'] = total

with pandas.option_context('display.max_rows', 1000,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df)

fig, axes = plt.subplots(figsize=(20, 10))
axes.barh(df.name, df.duration, left=df.startTime, color=df.color)
plt.savefig('shifts.png')


