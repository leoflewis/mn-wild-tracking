from this import s
from unittest import loader
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader
from .models import Game, Roster, Player, Schedule

# Create your views here.

def index(request):
    context = {}
    return render(request, "../templates/home.html", context)

def roster(request):
    roster = Roster().get_roster()
    
    #for person in roster['roster']:
        #response.write(person['person']['fullName'] + " " + person['position']['name'])

    context = {'roster': roster}
    return render(request, "../templates/roster.html", context)

def player(request, player_id):
    player = Player().get_player(player_id)
    name = player['people'][0]['fullName']
    context ={'player':player, 'name':name}
    return render(request, "../templates/player.html", context)

def schedule(request):
    schedule = Schedule().get_schedule()
    context = {"schedule": schedule } 
    return render(request, "../templates/schedule.html", context)

def game(request):
    game = Game().get_game(2022010007)
    response = HttpResponse()
    response.write(game)
    return response

def about(request):
    return render(request, "../templates/about.html")