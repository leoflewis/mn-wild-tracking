from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('roster', views.roster, name='roster'),
    path('schedule', views.schedule, name='schedule'),
    path('game', views.game, name='game'),
    path('player', views.player, name='player')
]