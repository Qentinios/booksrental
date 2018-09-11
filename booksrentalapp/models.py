from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default=None, null=True)
    pub_date = models.DateField('date published')
    author = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Rent(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rent_date = models.DateTimeField('date rented')
    return_date = models.DateTimeField('date returned', default=None, null=True)

    def __str__(self):
        return self.book.title + " -> " + self.user.username


class Category(models.Model):
    category = models.CharField(max_length=200)
    slug = models.SlugField(default='no-slug', max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # save a slug if there is no slug or when it's 'no-slug' (the default slug)
        if not self.slug or self.slug == 'no-slug':
            self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category


class BookCategory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title + " -> " + self.category.category




