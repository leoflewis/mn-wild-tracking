from django.db import models
import requests

class Game(models.Model):
    def get_game(self, id):
        response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id))
        return response.json()

class Roster(models.Model):
    def get_roster(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30/roster")
        return response.text

class Player(models.Model):
    def get_player(self, id):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/people/{}/".format(id))
        return response.json()

class Schedule(models.Model):
    def get_schedule(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=30&season=20222023&gameType=R")
        return response.json()

class Home(models.Model):
        def get_team(self):
            response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30")
            return response.json()
