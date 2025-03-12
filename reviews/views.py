# reviews/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm
from .models import Review

def submit_review(request):
    """
    Allows users to submit a review.
    Reviews will be pending approval until an admin approves them.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_success')
        else:
            print("Form errors:", form.errors)  # Debug: Print form errors
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form})


def review_ticker(request):
    """
    Retrieves approved reviews and renders the review ticker template.
    """
    reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'reviews/review_ticker.html', {'reviews': reviews})

def review_success(request):
    """
    Displays a confirmation page after a review is submitted.
    """
    print("Review success view reached!")  # Debug: Print message to console
    return render(request, 'reviews/review_success.html')


