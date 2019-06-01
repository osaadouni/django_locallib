"""Catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreateView.as_view(), name='book-create'),
    #re_path(r'^book/(?P<pk>\d+)', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('book/<int:pk>/add_copy/', views.BookCopyAddView.as_view(), name='book-copy-add'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('author/<int:pk>/add_book/', views.AuthorBookAddView.as_view(), name='author-book-add'),

    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed-books'),
    path('librarian/', views.LibrarianListView.as_view(), name='librarian-view'),

    path('book/<uuid:pk>/return', views.BookReturnView.as_view(), name='book-return'),

    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

