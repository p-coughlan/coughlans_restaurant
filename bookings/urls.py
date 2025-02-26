# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('book/', views.book_table, name='book_table'),
    # Add more booking-related URL patterns as needed below...
]