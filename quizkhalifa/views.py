from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from .models import User
from .models import Game, GameInformation, Score
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
        score = 0
        game = get_object_or_404(Game, pk=game_id)
        questions = game.game_information.all()

        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option and selected_option == question.correct_answer:
                score += 1

        # Save the score
        Score.objects.create(user=request.user, game=game, score=score)

        # Optionally, you might want to redirect to a leaderboard or results page
        return render(request, 'quiz-templates/results.html', {'score': score, 'total': questions.count()})

    else:
        return HttpResponseRedirect(reverse('home'))


def game_leaderboard(request, game_id):
    # Fetch top 10 scores for a specific game
    top_scores = Score.objects.filter(game__id=game_id).order_by('-score')[:10]
    return render(request, 'quiz-templates/leaderboard.html', {'top_scores': top_scores, 'game_id': game_id})


def global_leaderboard(request):
    # Fetch top 10 scores across all games
    top_scores = Score.objects.all().order_by('-score')[:10]
    return render(request, 'quiz-templates/leaderboard.html', {'top_scores': top_scores})
