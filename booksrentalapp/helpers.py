from django.http import Http404

from booksrentalapp.models import Rent, Book


def book_if_exist(book_id):
    try:
        return Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")


def book_cut_description(books):
    for book in books:  # Cut description
        book.description = (book.description[:75] + '..') if len(book.description) > 75 else book.description
    return books


def book_already_rented(book_id):
    if Rent.objects.filter(book_id=book_id, return_date__isnull=True).exists():
        return True
    return False
