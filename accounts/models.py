from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    favorite_band = models.CharField(max_length=100, blank=True)
    favorite_cheese = models.CharField(max_length=100, blank=True)
    lucky_number = models.IntegerField()
