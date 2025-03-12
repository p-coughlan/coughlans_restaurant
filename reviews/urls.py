# reviews/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_review, name='submit_review'),
    path('ticker/', views.review_ticker, name='review_ticker'),
    path('review-success/', views.review_success, name='review_success'),
    # Add more review-related URL patterns as needed below...
]
