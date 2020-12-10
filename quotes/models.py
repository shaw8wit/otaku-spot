from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    data = models.ManyToManyField('Data', blank=True, related_name='quoteData')


class Data(models.Model):
    anime = models.CharField(max_length=50)
    character = models.CharField(max_length=50)
    quote = models.CharField(max_length=1000)
    user = models.ManyToManyField(User, blank=True, related_name='likedBy')

    def __str__(self):
        return f"{self.anime} : {self.character} -> {self.quote}"
