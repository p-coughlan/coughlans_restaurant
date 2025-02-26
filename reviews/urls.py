# reviews/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('ticker/', views.review_ticker, name='review_ticker'),
    # Add more review-related URL patterns as needed below...
]
