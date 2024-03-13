from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="app-home"),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('results/<int:score>/', views.results, name='results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('games/<int:game_id>/submit/', views.quiz_submit, name='quiz_submit')

]
