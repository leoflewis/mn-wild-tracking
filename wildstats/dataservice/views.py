import json
from this import s
from unittest import loader
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader
from .models import Game, Roster, Player, Schedule, Home, Stats
# Create your views here.

def index(request):
    home = Home().get_team()
    context = {
        "home": home,
        "name": home['teams'][0]['name']
    }
    return render(request, "../templates/home.html", context)

def roster(request):
    roster = Roster().get_roster()
    context = {"roster": roster["roster"]}
    return render(request, "../templates/roster.html", context)

def player(request, player_id):
    player = Player().get_player(player_id)
    name = player['people'][0]['fullName']
    context ={'player':player, 'name':name}
    return render(request, "../templates/player.html", context)

def schedule(request):
    schedule = Schedule().get_schedule()
    context = {"schedule": schedule['dates'] } 
    return render(request, "../templates/schedule.html", context)

def game(request):
    game = Game().get_game(2022010007)
    response = HttpResponse()
    response.write(game)
    return response

def team_stats(request):
    stats = Stats().get_team_stats()
    context = {"team_stats":stats["stats"][0]["splits"]}
    return render(request, "../templates/stats.html", context)

def about(request):
    return render(request, "../templates/about.html")