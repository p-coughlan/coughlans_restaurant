# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .forms import BookingForm
from .models import Booking
from datetime import datetime, timedelta
from reviews.models import Review

# GROUP FUNCTIONS BY RELATED TASKS
# The views should be grouped by related tasks: home page, booking form, and booking management.

def home(request):
    """
    Displays the home page with approved reviews.
    """
    approved_reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'bookings/home.html', {'approved_reviews': approved_reviews})

# -----------------------------------------------------------------------------

def book_table(request):
    """
    Displays the booking form and processes form submissions.
    Checks that the new booking does not exceed capacity.
    On success, saves the booking, sends a confirmation email, and redirects to the success page.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            total_reserved = check_capacity(booking)
            allowed_capacity = 40  # For example, 80% of a 50-seat restaurant
            if total_reserved + booking.guests > allowed_capacity:
                form.add_error(None, "Cannot accept booking: The requested time slot is nearly full.")
                return render(request, 'bookings/book_table.html', {
                    'form': form,
                    'timeslots': available_timeslots()
                })
            booking.save()
            messages.success(request, f"Booking for {booking.date} at {booking.time} confirmed!")
            send_mail(
                subject="Your Booking Confirmation",
                message=(f"Dear {booking.customer.name},\n\n"
                         f"Your booking for {booking.date} at {booking.time} is confirmed.\n"
                         "We look forward to welcoming you at Coughlan's!\n\n"
                         "Thank you."),
                from_email="noreply@coughlans.com",
                recipient_list=[booking.customer.email],
                fail_silently=False,
            )
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()
    
    # Pass available timeslots to the template
    return render(request, 'bookings/book_table.html', {
        'form': form,
        'timeslots': available_timeslots()
    })


def check_capacity(new_booking):
    """
    For a given new_booking instance (unsaved), this function calculates
    the total number of guests already reserved for bookings whose 2-hour window
    overlaps with the new_booking's 2-hour window.
    """
    booking_date = new_booking.date
    new_start = datetime.combine(booking_date, new_booking.time)
    new_end = new_start + timedelta(hours=2)

    # Get all bookings for that date
    existing_bookings = Booking.objects.filter(date=booking_date)
    total_reserved = 0

    for booking in existing_bookings:
        existing_start = datetime.combine(booking.date, booking.time)
        existing_end = existing_start + timedelta(hours=2)
        # Check if the new booking overlaps with the existing booking's 2-hour window:
        if new_start < existing_end and existing_start < new_end:
            total_reserved += booking.guests

    return total_reserved

# Helper function to return a list of available timeslots for demonstration purposes
# To be replaced with a real-time availability check in a production system
def available_timeslots():
    """
    Returns a list of available timeslots for demonstration purposes.
    Each timeslot is represented as a dictionary with a 'time' and an 'available' flag.
    """
    return [
        {'time': '18:00', 'available': True},
        {'time': '18:30', 'available': False},
        {'time': '19:00', 'available': True},
        {'time': '19:30', 'available': True},
        {'time': '20:00', 'available': False},
    ]


def booking_success(request, booking_id):
    """
    Displays the booking success page with details for the given booking.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

def manage_booking(request, booking_id):
    """
    Allows a customer to update or cancel their booking.
    
    The view displays the current booking details and a form pre-populated with
    booking data. The form includes two buttons: one to update and one to cancel
    the booking. Based on the 'action' value from the submitted form, the view
    either updates the booking or deletes it.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update':
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()
                messages.success(request, "Your booking has been updated successfully!")
                return redirect('booking_success', booking_id=booking.id)
            else:
                messages.error(request, "Please correct the errors below.")
        
        elif action == 'cancel':
            booking.delete()
            messages.success(request, "Your booking has been cancelled.")
            return redirect('home')
        
        else:
            # If no valid action is specified, re-display the form with an error.
            form = BookingForm(instance=booking)
            messages.error(request, "No valid action was selected.")
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'bookings/manage_booking.html', {
        'form': form,
        'booking': booking
    })