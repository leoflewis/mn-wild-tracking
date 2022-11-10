from re import A
from django.db import models
from matplotlib import pyplot as plt 
import requests
from os.path import exists
import io, base64, json


class Game(models.Model):
    def get_game(self, id):
        response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id))
        return response.json()
    
    def make_figure(self, id):
        fig, axes = plt.subplots(figsize=(20, 10))
        #axes = plt.axes()
        axes.set_aspect(1)
        circle = plt.Circle((0,0),150, facecolor='none', edgecolor='gray', fill='true')
        axes.add_artist(circle)

        circle = plt.Circle((-690,220),150, facecolor='none', edgecolor='gray', fill='true')
        axes.add_artist(circle)

        circle = plt.Circle((690,220),150, facecolor='none', edgecolor='gray', fill='white')
        axes.add_artist(circle)

        circle = plt.Circle((690,-220),150,facecolor='none', edgecolor='gray', fill='white')
        axes.add_artist(circle)

        circle = plt.Circle((-690,-220),150, facecolor='none', edgecolor='gray', fill='white')
        axes.add_artist(circle)


        plt.plot(0, 0, marker='o', color='gray')

        plt.plot(-690, 220, marker='o', color='gray')
        plt.plot(690, 220, marker='o', color='gray')
        plt.plot(690, -220, marker='o', color='gray')
        plt.plot(-690, -220, marker='o', color='gray')

        plt.plot(200, -220, marker='o', color='gray')
        plt.plot(-200, -220, marker='o', color='gray')
        plt.plot(-200, 220, marker='o', color='gray')
        plt.plot(200, 220, marker='o', color='gray')

        center_x = [0,0]
        center_y = [-425.0, 425.0]
        plt.plot(center_x, center_y,  color='gray')

        left_x = [-250,-250]
        left_y = [-425.0, 425.0]
        plt.plot(left_x, left_y,  color='gray')

        right_x = [250,250]
        right_y = [-425.0, 425.0]
        plt.plot(right_x, right_y,  color='gray')

        left_x = [-890,-890]
        left_y = [-425.0, 425.0]
        plt.plot(left_x, left_y,  color='gray')

        right_x = [890,890]
        right_y = [-425.0, 425.0]
        plt.plot(right_x, right_y,  color='gray')

        circle = plt.Circle((890,0),50,  color='gray')
        axes.add_artist(circle)


        circle = plt.Circle((-890,0),50, color='gray')
        axes.add_artist(circle)

        response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id))
        data = response.json()
        game = data['gameData']['game']['pk']
        home = data['gameData']['teams']['home']['triCode']
        away = data['gameData']['teams']['away']['triCode']
        home_goals_x, home_goals_y = [], []
        away_goals_x, away_goals_y = [], []
        
        home_shots_x, home_shots_y = [], []
        away_shots_x, away_shots_y = [], []

        home_A_shots_x, home_A_shots_y = [], []
        away_A_shots_x, away_A_shots_y = [], []
        
        for play in data['liveData']['plays']['allPlays']:
            period = play['about']['period']
            if play['result']['event'] == 'Goal':
                if play['team']['triCode'] == home:
                    x_coord = play['coordinates']['x'] * 10
                    y_coord = play['coordinates']['y'] * 10
                    if period == 2 or period == 4:
                        x_coord = x_coord * -1
                        y_coord = y_coord * -1
                    home_goals_x.append(int(x_coord))
                    home_goals_y.append(int(y_coord))
                    plt.text(x_coord, y_coord, str(play['players'][0]['player']['fullName']))
                if play['team']['triCode'] == away:
                    x_coord = play['coordinates']['x'] * 10
                    y_coord = play['coordinates']['y'] * 10
                    if period == 2 or period == 4:
                        x_coord = x_coord * -1
                        y_coord = y_coord * -1
                    away_goals_x.append(int(x_coord))
                    away_goals_y.append(int(y_coord))
                    plt.text(x_coord, y_coord, str(play['players'][0]['player']['fullName']))
            if play['result']['event'] == 'Shot':
                if play['team']['triCode'] == home:
                    x_coord = play['coordinates']['x'] * 10
                    y_coord = play['coordinates']['y'] * 10
                    if period == 2 or period == 4:
                        x_coord = x_coord * -1
                        y_coord = y_coord * -1
                    home_shots_x.append(x_coord)
                    home_shots_y.append(y_coord)
                if play['team']['triCode'] == away:
                    x_coord = play['coordinates']['x'] * 10
                    y_coord = play['coordinates']['y'] * 10
                    if period == 2 or period == 4:
                        x_coord = x_coord * -1
                        y_coord = y_coord * -1
                    away_shots_x.append(x_coord)
                    away_shots_y.append(y_coord)
            if play['result']['event'] == 'Missed Shot':
                if play['team']['triCode'] == home:
                    x_coord = play['coordinates']['x'] * 10
                    y_coord = play['coordinates']['y'] * 10
                    if period == 2 or period == 4:
                        x_coord = x_coord * -1
                        y_coord = y_coord * -1
                    home_A_shots_x.append(x_coord)
                    home_A_shots_y.append(y_coord)
                    #plt.plot(x_coord, y_coord, marker='x', color='blue')
                if play['team']['triCode'] == away:
                    x_coord = play['coordinates']['x'] * 10
                    y_coord = play['coordinates']['y'] * 10
                    if period == 2 or period == 4:
                        x_coord = x_coord * -1
                        y_coord = y_coord * -1
                    away_A_shots_x.append(x_coord)
                    away_A_shots_y.append(y_coord)
                    #plt.plot(x_coord, y_coord, marker='x', color='red')
        plt.scatter(home_goals_x, home_goals_y, marker='o', label='home goal', color='blue')
        plt.scatter(away_goals_x, away_goals_y, marker='o', label='away goal', color='red')

        plt.scatter(home_shots_x, home_shots_y, marker='^', label='home shot', color='blue')
        plt.scatter(away_shots_x, away_shots_y, marker='^', label='away shot', color='red')

        plt.scatter(home_A_shots_x, home_A_shots_y, marker='x', label='home shot attempt', color='blue')
        plt.scatter(away_A_shots_x, away_A_shots_y, marker='x', label='away shot attempt', color='red')

        plt.title(away + " at " + home)
        plt.legend(loc="upper right", ncol=2)
        #loc='upper left', numpoints=1, , fontsize=8, bbox_to_anchor=(0, 0)
        plt.axis("off")
        
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue())
        plt.close(fig)
        return "data:image/png;base64, {}".format(encoded.decode('utf-8'))
        

    def compute_corsi(self, game_id):
        response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(game_id))
        data = response.json()
        #print(data['liveData']['plays']['allPlays'])
        if data['liveData']['plays']['allPlays'] == []:
            return []
        lines = []
        home = data['gameData']['teams']['home']['triCode']
        away = data['gameData']['teams']['away']['triCode']
        home_proper_shots = 0
        home_attempt_shots = 0
        home_block_shots = 0
        home_corsi_shots = 0
        away_proper_shots = 0
        away_attempt_shots = 0
        away_block_shots = 0
        away_corsi_shots = 0
        for play in data['liveData']['plays']['allPlays']:
            if play['result']['event'] == 'Shot' or play['result']['event'] == 'Goal':
                if play['team']['triCode'] == home:
                    home_proper_shots += 1
                if play['team']['triCode'] == away:
                    away_proper_shots += 1
            if play['result']['event'] == 'Blocked Shot':
                if play['team']['triCode'] == home:
                    home_block_shots += 1
                if play['team']['triCode'] == away:
                    away_block_shots += 1
            if play['result']['event'] == 'Missed Shot':
                if play['team']['triCode'] == home:
                    home_attempt_shots += 1
                if play['team']['triCode'] == away:
                    away_attempt_shots += 1

        home_corsi_shots = away_block_shots + home_attempt_shots + home_proper_shots
        away_corsi_shots = home_block_shots + away_attempt_shots + away_proper_shots

        home_fenwick_shots = home_attempt_shots + home_proper_shots
        away_fenwick_shots = away_attempt_shots + away_proper_shots

        total_corsi = home_corsi_shots + away_corsi_shots
        total_shots = home_proper_shots + away_proper_shots
        total_fenwick = home_attempt_shots + home_proper_shots + away_attempt_shots + away_proper_shots

        corsi_json = {}
        corsi_json['home_shots'] = home_proper_shots
        corsi_json['home_blocks'] = home_block_shots
        corsi_json['home_corsi_for'] = home_corsi_shots
        corsi_json['home_fenwick_for'] = home_fenwick_shots
        
        corsi_json['away_shots'] = away_proper_shots
        corsi_json['away_blocks'] = away_block_shots
        corsi_json['away_corsi_for'] = away_corsi_shots
        corsi_json['away_fenwick_for'] = away_fenwick_shots

        if total_shots > 0:
            corsi_json['home_shot_share'] = round((home_proper_shots / total_shots) * 100, 2)
            corsi_json['away_shot_share'] = round((away_proper_shots / total_shots) * 100, 2)

        if total_corsi > 0:
            corsi_json['home_corsi_share'] = round((home_corsi_shots / total_corsi) * 100, 2)
            corsi_json['away_corsi_share'] = round((away_corsi_shots / total_corsi) * 100, 2)

        if total_fenwick > 0:
            corsi_json['home_fenwick_share'] = round((home_fenwick_shots/ total_fenwick) * 100, 2)
            corsi_json['away_fenwick_share'] = round((away_fenwick_shots / total_fenwick) * 100, 2)

        return corsi_json

    def chart_corsi(self, id):
        response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id))
        data = response.json()

        home = data['gameData']['teams']['home']['triCode']
        away = data['gameData']['teams']['away']['triCode']
        time = 0 
        home_shots = 0
        away_shots = 0
        fig = plt.figure(1)
        for play in data['liveData']['plays']['allPlays']:
            period = play['about']['period']
            if play['result']['event'] == 'Goal':
                if play['team']['triCode'] == home:
                    time = convert_time(play['about']['periodTime'], period)
                    home_shots += 1
                    plt.plot(time, home_shots,marker='o', color='blue')
                if play['team']['triCode'] == away:
                    time = convert_time(play['about']['periodTime'], period)
                    away_shots += 1
                    plt.plot(time, away_shots, marker='o', color='red')
            if play['result']['event'] == 'Shot':
                if play['team']['triCode'] == home:
                    time = convert_time(play['about']['periodTime'], period)
                    home_shots += 1
                    plt.plot(time, home_shots, marker='^', color='blue')
                if play['team']['triCode'] == away:
                    time = convert_time(play['about']['periodTime'], period)
                    away_shots += 1
                    plt.plot(time, away_shots, marker='^', color='red')
        plt.ylabel("Shots + Goals")
        plt.xlabel("Time")
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue())
        plt.close(fig)
        return "data:image/png;base64, {}".format(encoded.decode('utf-8'))

def convert_time(time, period):
    if period == 2:
        return 20 + (int(time[0:2]) + (int(time[3:5]) / 100))
    if period == 3:
        return 40 + (int(time[0:2]) + (int(time[3:5]) / 100))
    if period == 4:
        return 60 + (int(time[0:2]) + (int(time[3:5]) / 100))
    return (int(time[0:2]) + (int(time[3:5]) / 100))

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

