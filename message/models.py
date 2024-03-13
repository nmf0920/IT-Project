from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MessageDetails(models.Model):
    sender = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    messageBody = models.TextField()

    def __str__(self) -> str:
        return self.messageBody