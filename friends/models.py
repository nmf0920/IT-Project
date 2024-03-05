from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Fren(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    friendname = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.friendname
 