from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Game

# Create your views here.

def index(request):
    response = str(Game().get_game(2022010007))
    
    return HttpResponse(response)