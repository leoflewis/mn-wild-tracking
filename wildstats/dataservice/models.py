from re import A
from django.db import models
import requests

class Game(models.Model):
    def get_game(self, id):
        response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id))
        return response.json()
    
    def parse_game_data(self, id):
        data = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id)).json()
        response = requests.get("https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={}".format(id))
        shifts = response.json()
        shifts= shifts['data']
        #return shifts['data']
        #team codes
        print(shifts)
        home = data['gameData']['teams']['home']['triCode']
        away = data['gameData']['teams']['away']['triCode']
        shift_count = 0
        lines = []
        #each play
        for play in data['liveData']['plays']['allPlays']:
            #exclude certain event types because they are useless
            event = play['result']['event']
            if event != 'Game Scheduled' and event != 'Period Ready' and event != 'Period Start' and event != 'Game Official' and event != 'Game End' and event != 'Period End' and event != 'Period Official':
                #periods need to match on play and shift
                period = play['about']['period']
                play_time = play['about']['periodTime']
                if len(shifts) == 0:
                    return []
                #check each shift
                home_names = home + " - "
                away_names = away + " - "
                home_state = 0
                away_state = 0
                for shift in shifts:
                    #pull start and end time
                    shift_start = shift['startTime']
                    shift_end = shift['endTime']
                    
                    #exclude where shift starts at the same time play stopped and where shift ends at the same time as a faceoff
                    if shift['period'] == period and (play_time >= shift_start and play_time <= shift_end):
                        
                        if not ((event == "Stoppage" and play_time == shift_start) or (event == "Faceoff" and play_time == shift_end) or (event == "Penalty" and play_time == shift_start) or (event == "Goal" and play_time == shift_start) or (event == "Hit" and play_time == shift_end) or (event == "Giveaway" and play_time == shift_end)):
                            #log home team on ice
                            if shift['teamAbbrev'] == home:
                                home_names += shift['lastName'] + ", " 
                                home_state += 1
                            #log away team on ice
                            if shift['teamAbbrev'] == away:
                                away_names += shift['lastName'] + ", "
                                away_state += 1
                home_names += " -  on ice for " + play['result']['event'] + " at " + play_time + " in " + str(period)
                away_names += " -  on ice for " + play['result']['event'] + " at " + play_time + " in " + str(period)
                #home v away
                state = str(home_state) + "v" + str(away_state)
                lines.append(home_names)
                lines.append(away_names)
                lines.append(state)
                shift_count += 1
            lines.append("")
        lines.append((shift_count))
        return lines

class Roster(models.Model):
    def get_roster(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30/roster")
        return response.json()

class Player(models.Model):
    def get_player(self, id):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/people/{}/".format(id))
        return response.json()

    def get_player_stats(self, id):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=yearByYear".format(id))
        return response.json()

class Schedule(models.Model):
    def get_schedule(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=30&season=20222023&gameType=R")
        return response.json()

class Home(models.Model):
    def get_team(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30")
        return response.json()

class Stats(models.Model):
    def get_team_stats(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30/stats")
        return response.json()

