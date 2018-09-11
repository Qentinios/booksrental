from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from booksrentalapp import helpers
from booksrentalapp.models import Category, Book, Rent
from django.contrib import messages


def main(request):
    books = Book.objects.order_by('-pub_date')
    return show_library(request, books)


def category(request, slug):
    books = Book.objects.filter(bookcategory__category__slug=slug).order_by('-pub_date')
    return show_library(request, books)


def show_library(request, books):
    categories = Category.objects.all()  # Get all categories

    books_pagination = Paginator(books, 6)  # Show 6 books per page
    page = request.GET.get('page')
    books = books_pagination.get_page(page)

    books = helpers.book_cut_description(books)

    template = loader.get_template('booksrentalapp/library.html')
    context = {
        'categories': categories,
        'books': books,
    }
    return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'booksrentalapp/signup.html', {'form': form})


def book_detail(request, book_id):
    book = helpers.book_if_exist(book_id)
    book.rented = helpers.book_already_rented(book_id)

    return render(request, 'booksrentalapp/book.html', {'book': book})


@login_required
def profile(request):
    book_ids = Rent.objects.filter(user=request.user, return_date__isnull=True).values_list('book_id', flat=True)
    books = Book.objects.filter(id__in=book_ids)

    return render(request, 'booksrentalapp/profile.html', {'books': books})


@login_required
def return_book(request, book_id):
    book = helpers.book_if_exist(book_id)

    rents = Rent.objects.filter(user=request.user, book=book_id, return_date__isnull=True)

    if not rents:
        messages.add_message(request, messages.ERROR, 'Book is not rented by you: ' + book.title)
        return redirect('/profile/')

    for rent in rents:
        rent.return_date = timezone.now()
        rent.save()

    messages.add_message(request, messages.WARNING, 'Returned book: ' + book.title)
    return redirect('/profile/')


@login_required
def rent_book(request, book_id):
    book = helpers.book_if_exist(book_id)

    if helpers.book_already_rented(book_id):
        messages.add_message(request, messages.ERROR, 'Book is not available: ' + book.title)
        return redirect('/book/' + str(book_id))

    messages.add_message(request, messages.SUCCESS, 'Rented book: ' + book.title)

    rent = Rent(book=book, user=request.user, rent_date=timezone.now())
    rent.save()

    return redirect('/profile')


