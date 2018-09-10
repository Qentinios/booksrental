from django.conf import settings
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default=None, null=True)
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=40)


class Rent(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rent_date = models.DateTimeField('date rented')
    return_date = models.DateTimeField('date returned', default=None, null=True)


class Category(models.Model):
    category = models.CharField(max_length=200)


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




