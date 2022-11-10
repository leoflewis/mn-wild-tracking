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
        "home": home
    }
    return render(request, "../templates/home.html", context)

def roster(request):
    roster = Roster().get_roster()
    context = {"roster": roster["roster"]}
    return render(request, "../templates/roster.html", context)

def player(request, player_id):
    player = Player().get_player(player_id)
    stats = Player().get_player_stats(player_id)
    current_season = stats['stats'][0]['splits'][len(stats['stats'][0]['splits'])-1]
    context ={"player": player, "stats": stats['stats'], "current_season": current_season}
    if(player['people'][0]['primaryPosition']['type']) != 'Goalie':
        return render(request, "../templates/player.html", context)
    else:
        return render(request, "../templates/goalie.html", context)

def schedule(request):
    schedule = Schedule().get_schedule()
    context = {"schedule": schedule['dates'] } 
    return render(request, "../templates/schedule.html", context)

def game(request, game_id):
    game = Game().get_game(game_id)
    corsi = Game().compute_corsi(game_id)
    pic = Game().make_figure(game_id)
    chart = Game().chart_corsi(game_id)
    context = {"game" : game, "corsi": corsi, "fig": pic, "chart": chart}
    return render(request, "../templates/game.html", context)

def team_stats(request):
    stats = Stats().get_team_stats()
    context = {"team_stats":stats["stats"][0]["splits"]}
    return render(request, "../templates/stats.html", context)

def about(request):
    return render(request, "../templates/about.html")