import requests, matplotlib.pyplot as plt, numpy as np, pandas

def convert_start_time(time, period):
    period = int(period)
    if period == 2:
        return 20 + (int(time[0:2]) + (int(time[3:5]) / 100))
    if period == 3:
        return 40 + (int(time[0:2]) + (int(time[3:5]) / 100))
    if period == 4:
        return 60 + (int(time[0:2]) + (int(time[3:5]) / 100))
    return (int(time[0:2]) + (int(time[3:5]) / 100))


id = 2022020283
response = requests.get("https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={}".format(id))
shifts = response.json()['data']

df = pandas.DataFrame(shifts)
df = df.astype(str)
df['name'] = df.firstName + " " + df.lastName

df.drop(['eventDescription', 'detailCode', 'eventDetails', 'typeCode', 'gameId', 'shiftNumber', 'teamName', 'hexValue', 'id', 'eventNumber', 'teamId', 'firstName', 'lastName'], axis=1, inplace=True)
df = df.astype(str)

print(df.dtypes)
print(df.columns)
print(df)

fig, ax = plt.subplots(1)
ax.barh(df.name, df.duration, left=df.startTime)
plt.show()



