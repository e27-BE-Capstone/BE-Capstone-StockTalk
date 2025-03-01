from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    image = models.URLField(default='images/default-photo.jpg')
    bio = models.TextField(max_length=300)
    reputation = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)