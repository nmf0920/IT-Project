from django.db import models

# Create your models here.
# class User(models.Model):
#     userID = models.AutoField(primary_key=True)
#     username = models.TextField(blank=True)
#     email = models.TextField(blank=True)
#     password = models.TextField()


class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GameInformation(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name='game_information')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        default='A')

    def __str__(self):
        return self.question_text

    def get_options(self):

        options = [
            ('A', self.option_a),
            ('B', self.option_b),
            ('C', self.option_c),
            ('D', self.option_d),
        ]
        return options
