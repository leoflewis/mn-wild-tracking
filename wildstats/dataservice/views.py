from this import s
from unittest import loader
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import loader
from .models import Game, Roster, Player, Schedule

# Create your views here.

def index(request):
    return HttpResponse("")

def roster(request):
    roster = Roster().get_roster()
    response = HttpResponse()
    for person in roster['roster']:
        response.write(person['person']['fullName'] + " " + person['position']['name'])
    return response

def player(request, player_id):
    player = Player().get_player(player_id)
    name = player['people'][0]['fullName']
    context ={'player':player, 'name':name}
    return render(request, "../templates/player.html", context)

def schedule(request):
    schedule = Schedule().get_schedule()
    response = HttpResponse()
    response.write(schedule)
    return response

def game(request):
    game = Game().get_game(2022010007)
    response = HttpResponse()
    response.write(game)
    return response