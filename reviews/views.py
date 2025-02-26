# reviews/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm
from .models import Review

def submit_review(request):
    """
    Allows users to submit a review using the revised ReviewForm.
    The review is saved (pending admin approval) and a success message is displayed and the user is redirected to the home page.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your review! It will appear once approved.")
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'reviews/submit_review.html', {'form': form})

def review_ticker(request):
    """
    Retrieves approved reviews and renders the review ticker template.
    """
    reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'reviews/review_ticker.html', {'reviews': reviews})
