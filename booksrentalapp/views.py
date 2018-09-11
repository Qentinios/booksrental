from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from booksrentalapp.models import Category, Book
from django.contrib import messages


def main(request):
    books = Book.objects.order_by('-pub_date')
    return show_library(request, books)


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
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    return render(request, 'booksrentalapp/book.html', {'book': book})


@login_required
def profile(request):
    messages.add_message(request, messages.INFO, 'Welcome ' + request.user.username)
    books = Book.objects.all()
    return render(request, 'booksrentalapp/profile.html', {'books': books})


def category(request, slug):
    books = Book.objects.filter(bookcategory__category__slug=slug).order_by('-pub_date')
    return show_library(request, books)


def show_library(request, books):
    categories = Category.objects.all()  # Get all categories

    books_pagination = Paginator(books, 6)  # Show 6 books per page
    page = request.GET.get('page')
    books = books_pagination.get_page(page)

    for book in books:  # Cut description
        book.description = (book.description[:75] + '..') if len(book.description) > 75 else book.description

    template = loader.get_template('booksrentalapp/library.html')

    context = {
        'categories': categories,
        'books': books,
    }
    return HttpResponse(template.render(context, request))


@login_required
def return_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    # return

    messages.add_message(request, messages.SUCCESS, 'Rented book: ' + book.title)
    pass


@login_required
def rent_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    
    # rent

    messages.add_message(request, messages.SUCCESS, 'Returned book: ' + book.title)
    pass
