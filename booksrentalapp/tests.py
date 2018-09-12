from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.utils import timezone
from booksrentalapp.models import Book


class BookTestCase(TestCase):
    def setUp(self):
        # create books
        Book.objects.create(title="test", description="test description", pub_date=timezone.now(), author="test author")

        # create account
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.client = Client()
        self.client.login(username='temporary', password='temporary')

    def test_book_login(self):
        # Check response code
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    # rent
    def test_book_rent(self):
        response = self.client.get('/rent/1', follow=True)
        self.assertContains(response, 'alert-success" role="alert">Rented book: test')

    def test_already_rented_book_rent(self):
        self.client.get('/rent/1', follow=True)
        response = self.client.get('/rent/1', follow=True)
        self.assertContains(response, 'alert-danger" role="alert">Book is not available: test')

    def test_book_doesnt_exist_rent(self):
        response = self.client.get('/rent/100', follow=True)
        self.assertEqual(response.status_code, 404)

    # return
    def test_book_return(self):
        self.client.get('/rent/1', follow=True)
        response = self.client.get('/return/1', follow=True)
        self.assertContains(response, 'alert-warning" role="alert">Returned book: test')

    def test_book_doesnt_exist_return(self):
        response = self.client.get('/return/100', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_book_not_rented_return(self):
        response = self.client.get('/return/1', follow=True)
        self.assertContains(response, 'alert-danger" role="alert">Book is not rented by you: test')

    def test_book_not_rented_by_me_return(self):
        self.client.get('/rent/1', follow=True)

        self.create_second_user()

        response = self.client.get('/return/1', follow=True)

        self.assertContains(response, 'alert-danger" role="alert">Book is not rented by you: test')

    def create_second_user(self):
        get_user_model().objects.create_user('temporary2', 'temporary2@gmail.com', 'temporary2')

        self.client.logout()
        self.client = Client()
        self.client.login(username='temporary2', password='temporary2')
