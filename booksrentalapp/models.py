from django.conf import settings
from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=40)


class Rent(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
