from django.db import models
from django.contrib.auth.models import User, Group

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    

