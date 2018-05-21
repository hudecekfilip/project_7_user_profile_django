from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatar_photos/', default=None)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    animal = models.CharField(max_length=50, blank=True)
    hobby = models.TextField(blank=True)


    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email
