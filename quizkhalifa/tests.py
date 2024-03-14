from django.test import TestCase
from django.contrib.auth.models import User
from quizkhalifa.models import Game, GameInformation, Score
from django.urls import reverse
from users.forms import UserRegisterForm


class GameModelTest(TestCase):
    def test_game_creation(self):
        game = Game.objects.create(title="Trivia", description="Trivia Game")
        self.assertEqual(game.title, "Trivia")
        self.assertIn("Trivia", game.description)


class GameInformationModelTest(TestCase):
    def test_game_information_creation(self):
        game = Game.objects.create(title="Trivia", description="A Trivia Game")
        game_info = GameInformation.objects.create(
            game=game,
            question_text="What is the capital of France?",
            option_a="Paris",
            option_b="London",
            option_c="Berlin",
            option_d="Madrid",
            correct_answer="A"
        )
        self.assertEqual(game_info.question_text,
                         "What is the capital of France?")
        self.assertEqual(game_info.get_options()[0][1], "Paris")


class ScoreModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.game = Game.objects.create(
            title="Trivia", description="A Trivia Game")

    def test_score_creation(self):
        score = Score.objects.create(user=self.user, game=self.game, score=10)
        self.assertEqual(score.score, 10)


class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('app-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz-templates/home.html')


class RegisterViewTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('user-register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user-templates/register.html')

    def test_register_view_post(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ValidPassword123',
            'password2': 'ValidPassword123',

        }
        response = self.client.post(reverse('user-register'), form_data)
        self.assertEqual(response.status_code, 302,
                         f"Expected redirect to login, got {response.status_code}. Form errors: {response.context['form'].errors if response.context else 'N/A'}")


class UserRegisterFormTest(TestCase):
    def test_form_valid(self):
        form_data = {'username': 'newuser', 'email': 'user@example.com',
                     'password1': 'Testpassword123', 'password2': 'Testpassword123'}
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {'username': 'newuser',
                     'password1': 'testpassword', 'password2': 'wrongpassword'}
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())