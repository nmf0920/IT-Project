from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from .models import User
from .models import Game, GameInformation
from django.urls import reverse


def home(request):
    games = Game.objects.all()  # Fetch all game instances
    return render(request, 'quiz-templates/home.html', {'games': games})


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    # Accessing related game information
    game_information = game.game_information.all()
    return render(request, 'quiz-templates/game_detail.html', {'game': game, 'game_information': game_information})


def quiz_submit(request, game_id):
    if request.method == 'POST':
        # Process the submitted answers
        score = 0
        game = get_object_or_404(Game, pk=game_id)
        questions = game.game_information.all()

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_answer:
                score += 1

        # Redirect to a new URL or render a results page
        return render(request, 'quiz-templates/results.html', {'score': score, 'total': questions.count()})

    # Redirect if not a POST request, or handle as needed
    return HttpResponseRedirect(reverse('app-home'))
