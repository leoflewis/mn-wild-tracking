from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('roster', views.roster, name='roster'),
    path('schedule', views.schedule, name='schedule'),
    path('game/<int:game_id>', views.game, name='game'),
    path('player/<int:player_id>', views.player, name='player'),
    path('stats', views.team_stats, name='team stats'),
    path('about', views.about, name='about')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    print("pictuessss")
    