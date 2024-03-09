from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="app-home"),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('leaderboard/', views.global_leaderboard, name='global_leaderboard'),
    path('leaderboard/game/<int:game_id>/',
         views.game_leaderboard, name='game_leaderboard'),
    path('games/<int:game_id>/submit/', views.quiz_submit, name='quiz_submit')

]
