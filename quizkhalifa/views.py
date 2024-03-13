from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from .models import User
from .models import Game, GameInformation, Score
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
import requests
import random
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control

def home(request):
    games = Game.objects.all()  # Fetch all game instances
    return render(request, 'quiz-templates/home.html', {'games': games})


def fetch_trivia_questions(amount=10, category=9, difficulty='medium', question_type='multiple'):
    url = 'https://opentdb.com/api.php'
    params = {
        'amount': amount,
        'category': category,
        'difficulty': difficulty,
        'question_type': type
    }
    response = requests.get(url, params=params)
    print("Response status code:", response.status_code)  # Debug print
    if response.status_code == 200:
        data = response.json()
        print("Data received:", data)  # Debug print
        return data['results']
    else:
        print("Failed to fetch trivia questions")  # Debug print
        return []


# def game_detail(request, game_id):
#     game = get_object_or_404(Game, pk=game_id)
#     # Accessing related game information
#     game_information = game.game_information.all()
#     return render(request, 'quiz-templates/game_detail.html', {'game': game, 'game_information': game_information})

def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    difficulty_mapping = {
        'Easy': 'easy',
        'Medium': 'medium',
        'Hard': 'hard'
    }
    trivia_difficulty = difficulty_mapping.get(
        game.title, 'medium')
    print(trivia_difficulty)

    url = f'https://opentdb.com/api.php?amount=10&difficulty={trivia_difficulty}&type=multiple'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            questions = data.get('results', [])

            for question in questions:
                all_answers = question['incorrect_answers'] + \
                    [question['correct_answer']]
                random.shuffle(all_answers)
                question['all_answers'] = all_answers

            correct_answers = {str(
                index + 1): question['correct_answer'] for index, question in enumerate(questions)}
            request.session['correct_answers'] = correct_answers
            print(correct_answers)

            return render(request, 'quiz-templates/game_detail.html', {
                'game': game,
                'questions': questions
            })
        else:
            messages.error(
                request, "Failed to load trivia questions due to an API error. Please try again.")
            return redirect('app-home')
    except requests.exceptions.RequestException as e:

        messages.error(
            request, "Failed to fetch trivia questions. Please check your internet connection and try again.")
        return redirect('app-home')


# def quiz_submit(request, game_id):
#     if request.method == 'POST':
#         score = 0
#         game = get_object_or_404(Game, pk=game_id)
#         questions = game.game_information.all()

#         for question in questions:
#             selected_option = request.POST.get(f'question_{question.id}')
#             if selected_option and selected_option == question.correct_answer:
#                 score += 1

#         # Save the score
#         Score.objects.create(user=request.user, game=game, score=score)

#         # Optionally, you might want to redirect to a leaderboard or results page
#         return render(request, 'quiz-templates/results.html', {'score': score, 'total': questions.count()})

#     else:
#         return HttpResponseRedirect(reverse('home'))


def quiz_submit(request, game_id):
    if request.method == 'POST':
        print(request.POST)
        game = get_object_or_404(Game, pk=game_id)
        score = 0
        correct_answers = request.session.get('correct_answers', {})
        print(correct_answers)

        for question_id, correct_answer in correct_answers.items():
            # Assuming the name attribute for each question input is like "question_1", "question_2", etc.
            user_answer = request.POST.get(f'question_{question_id}')
            if user_answer == correct_answer:
                score += 1

        # Clear the correct answers from the session after scoring
        if 'correct_answers' in request.session:
            del request.session['correct_answers']

        # Redirect to a results page or render a template directly with the score
        # For example, redirecting to a generic "results" page (make sure to create this view and template)
        Score.objects.create(user=request.user, game=game, score=score)
        return HttpResponseRedirect(reverse('results', args=(score,)))

    else:
        # Redirect back to the game detail page if the method is not POST
        return redirect('game_detail', game_id=game_id)


def leaderboard(request):
    # Initialize a list to hold leaderboard data for each game
    global_top_scores = Score.objects.values('user__username').annotate(
        top_score=Max('score')).order_by('-top_score')[:10]

    games_leaderboards = []

    # Get all games
    games = Game.objects.all()

    # For each game, fetch the top scores
    for game in games:
        top_scores = Score.objects.filter(game=game).values('user__username').annotate(
            top_score=Max('score')).order_by('-top_score')[:10]
        games_leaderboards.append({'game': game, 'top_scores': top_scores})

    # You can also fetch global top scores here if needed

    return render(request, 'quiz-templates/leaderboard.html', {
        'games_leaderboards': games_leaderboards,
        'global_top_scores': global_top_scores,

    })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def results(request, score):
    total_questions = 10
    context = {'score': score, 'total_questions': total_questions}
    return render(request, 'quiz-templates/results.html', context)
