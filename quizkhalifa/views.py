from django.shortcuts import render
from django.http import HttpResponse
# from .models import User

games = [
    {
        'name': 'quiz 1',
        'duration': '5 mins',
        'difficulty': 'easy',
        'description': 'read the questions carefully and pick an answer from the options.'
    }, 
    {
        'name': 'quiz 2',
        'duration': '7 mins',
        'difficulty': 'medium',
        'description': 'observe the given pictures and select the odd one out from them.'
    }
]

def home(request):
    context = {
        'games': games
    }
    return render(request, 'quiz-templates/home.html', context)