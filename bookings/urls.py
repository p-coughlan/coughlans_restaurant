# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('book/', views.book_table, name='book_table'),
    path('success/<int:booking_id>/', views.booking_success, name='booking_success'), # th3 <int:booking_id> part of the URL pattern captures the booking_id value from the URL and passes it to the view function as an argument.
    path('manage/<int:booking_id>/', views.manage_booking, name='manage_booking'),
    path('weekly-calendar/', views.weekly_calendar, name='weekly_calendar'),
    path('daily-calendar/', views.daily_calendar, name='daily_calendar'),
    path('monthly-calendar/', views.monthly_calendar, name='monthly_calendar'),
    path('lunch-menu/', views.LunchMenuView.as_view(), name='lunch_menu'),
    path('dinner-menu/', views.DinnerMenuView.as_view(), name='dinner_menu'),
    # Path below surpluses the current requirements
    # path('manage-booking-lookup/', views.manage_booking_lookup, name='manage_booking_lookup'),
    path('manage-booking-lookup/', views.manage_booking_lookup_by_email, name='manage_booking_lookup_by_email'),
]