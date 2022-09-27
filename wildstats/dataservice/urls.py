from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('roster', views.roster, name='roster'),
    path('schedule', views.schedule, name='schedule'),
    path('game/<int:game_id>', views.game, name='game'),
    path('player/<int:player_id>', views.player, name='player')

]