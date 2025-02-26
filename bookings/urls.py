# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('book/', views.book_table, name='book_table'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'), # th3 <int:booking_id> part of the URL pattern captures the booking_id value from the URL and passes it to the view function as an argument.
    # Add more booking-related URL patterns as needed below...
]