# reviews/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm

def submit_review(request):
    """
    Allows users to submit a review using the revised ReviewForm.
    The review is saved (pending admin approval).
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
