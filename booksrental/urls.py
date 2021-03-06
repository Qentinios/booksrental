"""booksrental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from booksrentalapp import views as booksrentalapp_views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^signup/$', booksrentalapp_views.signup, name='signup'),
    url(r'admin/', admin.site.urls),
    url(r'^$', booksrentalapp_views.main),
    re_path('^category/(?P<slug>[\w-]+)/$', booksrentalapp_views.category, {}, name="category"),
    path('book/<int:book_id>/', booksrentalapp_views.book_detail, name='book'),
    path('profile/', booksrentalapp_views.profile, name='profile'),
    path('return/<int:book_id>/', booksrentalapp_views.return_book, name='return_book'),
    path('rent/<int:book_id>/', booksrentalapp_views.rent_book, name='rent_book'),
]
