from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.books),
    path('add', views.add),
    path('edit/<int:id>', views.edit),
    path('delete/<int:id>', views.delete),
    path('add_book', views.add_book),
    path('remove/<int:id>', views.remove)
]
