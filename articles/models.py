from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=40)
    content = models.CharField(max_length=1000)
    author = models.CharField(max_length=50)
