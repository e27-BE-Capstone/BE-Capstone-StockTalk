from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)
    description = models.TextField(blank=True, null=True)
    