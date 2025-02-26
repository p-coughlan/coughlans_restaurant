# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .forms import BookingForm
from .models import Booking
from datetime import datetime, timedelta

def home(request):
    """
    Displays the home page.
    """
    return render(request, 'bookings/home.html', {})


def book_table(request):
    """
    Displays the booking form and processes form submissions.
    Checks that the new booking does not exceed capacity.
    On success, saves the booking, sends a confirmation email, and redirects to a success page.
    The view first checks if the form was submitted (POST request).
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get an unsaved booking instance from the form (customer linking is done in the form's save method)
            booking = form.save(commit=False)
            
            # Check capacity: suppose allowed capacity is 40 (80% of a 50-seat restaurant)
            total_reserved = check_capacity(booking)
            allowed_capacity = 40
            if total_reserved + booking.guests > allowed_capacity:
                form.add_error(None, "Cannot accept booking: The requested time slot is nearly full.")
                return render(request, 'bookings/book_table.html', {'form': form})
            
            # Save the booking
            booking.save()
            messages.success(request, f"Booking for {booking.date} at {booking.time} confirmed!")
            
            # Send a confirmation email using customer details from the linked Customer
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

    return render(request, 'bookings/book_table.html', {'form': form})


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

def booking_success(request, booking_id):
    """
    Displays the booking success page with details for the given booking.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_success.html', {'booking': booking})