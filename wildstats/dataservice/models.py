from django.db import models
import sys
# Create your models here.

import requests

def get_roster():
    response = requests.get("https://statsapi.web.nhl.com/api/v1/teams/30/roster")
    return response

def get_schedule():
    response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=30&season=20222023")
    return response

def get_player(id):
    response = requests.get("https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=gameLog".format(id))
    return response


class Game(models.Model):
    game = None
    def get_game(self, id):
        response = requests.get("http://statsapi.web.nhl.com/api/v1/game/{}/feed/live".format(id))

        game = response.json()

        return str(game)