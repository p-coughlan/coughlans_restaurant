# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .forms import BookingForm, AdminBookingForm
from .models import Booking
from datetime import date, datetime, timedelta, time
from reviews.models import Review
from collections import OrderedDict
from django.contrib.admin.views.decorators import staff_member_required 
from django.views.generic import TemplateView 


# GROUP FUNCTIONS BY RELATED TASKS
# The views should be grouped by related tasks: home page, booking form, and booking management.

def home(request):
    """
    Displays the home page with approved reviews.
    """
    approved_reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'bookings/home.html', {'approved_reviews': approved_reviews})

# -----------------------------------------------------------------------------
# Booking Form

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

# -----------------------------------------------------------------------------
# Capacity Check

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

# -----------------------------------------------------------------------------
# Helper Functions

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

def get_day_timeslots(day):
    """
    For a given day (a date object), return a list of timeslots with their availability.
    Timeslots are generated in 30-minute increments from 18:00 to 21:00.
    Returns:
        A list of dictionaries with keys: 'time' (as a string) and 'available' (bool).
    """
    timeslot_list = []
    start_time = time(18, 0)  # Start at 18:00
    end_time = time(21, 0)    # End at 21:00
    current_datetime = datetime.combine(day, start_time)
    end_datetime = datetime.combine(day, end_time)
    
    while current_datetime <= end_datetime:
        timeslot_str = current_datetime.strftime("%H:%M")
        timeslot_list.append({'time': timeslot_str, 'available': True})
        current_datetime += timedelta(minutes=30)
    return timeslot_list

# -----------------------------------------------------------------------------
# Booking Success and Management

def booking_success(request, booking_id):
    """
    Displays the booking success page with details for the given booking.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

def manage_booking(request, booking_id):
    """
    Allows a user to update or cancel their booking.
    Uses AdminBookingForm for updating.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update':
            form = AdminBookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()
                messages.success(request, "Your booking has been updated successfully!")
                return redirect('booking_success', booking_id=booking.id)
            else:
                messages.error(request, "Please correct the errors below.")
                
        elif action == 'cancel':
            booking.delete()
            # Render the cancellation success template instead of using a Django message
            return render(request, 'bookings/cancel_success.html')
        else:
            form = AdminBookingForm(instance=booking)
            messages.error(request, "Invalid action selected.")
    else:
        form = AdminBookingForm(instance=booking)
    
    return render(request, 'bookings/manage_booking.html', {
        'form': form,
        'booking': booking
    })


# -----------------------------------------------------------------------------
# Booking Lookup

# def manage_booking_lookup(request):
#     """
#     Displays a simple form where a user can enter their booking ID to manage (update or cancel) their booking.
#     Upon submission, the user is redirected to the manage_booking view for that booking.
#     """
#     if request.method == "POST":
#         booking_id = request.POST.get("booking_id")
#         if booking_id:
#             return redirect('manage_booking', booking_id=booking_id)
#         else:
#             messages.error(request, "Please enter a valid booking ID.")
#     return render(request, 'bookings/manage_booking_lookup.html')

# ALTERNATE LOOKUP FUNCTION
# Instead of using an ID, the user can enter their email address and then query the database for bookings associated with that email address.
# This approach is more user-friendly and can be implemented as follows:

def manage_booking_lookup_by_email(request):
    """
    Displays a form for users to look up bookings by a customer's email address.
    If one booking is found, redirects to the manage booking page.
    If multiple bookings are found, displays a list for the user to choose from.
    If no bookings are found, an error message is included in the context.
    """
    bookings_found = None
    error_message = None
    
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if email:
            bookings_found = Booking.objects.filter(customer__email__iexact=email)
            if not bookings_found.exists():
                error_message = "No bookings found for that email address."
            elif bookings_found.count() == 1:
                booking = bookings_found.first()
                return redirect('manage_booking', booking_id=booking.id)
        else:
            error_message = "Please enter an email address."
    
    context = {
        'bookings_found': bookings_found,
        'error_message': error_message
    }
    return render(request, 'bookings/manage_booking_lookup.html', context)



# -----------------------------------------------------------------------------
# Staff-Only Views

@staff_member_required
def weekly_calendar(request):
    """
    Displays a weekly calendar view of bookings for staff.
    Determines the starting Monday from the 'week_start' GET parameter (YYYY-MM-DD),
    and collects bookings for each day of the week.
    """
    week_start_str = request.GET.get("week_start")
    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        except ValueError:
            week_start = date.today() - timedelta(days=date.today().weekday())
    else:
        week_start = date.today() - timedelta(days=date.today().weekday())
    
    # Collect bookings for each day of the week
    days = []
    for i in range(7):
        current_day = week_start + timedelta(days=i)
        daily_bookings = Booking.objects.filter(date=current_day).order_by('time')
        days.append({'day': current_day, 'bookings': daily_bookings})
    
    previous_week = week_start - timedelta(days=7)
    next_week = week_start + timedelta(days=7)
    
    context = {
        'week_start': week_start,
        'days': days,
        'previous_week': previous_week.strftime("%Y-%m-%d"),
        'next_week': next_week.strftime("%Y-%m-%d"),
    }
    return render(request, 'bookings/weekly_calendar.html', context)

# -----------------------------------------------------------------------------
# Lunch and Dinner Menus

class LunchMenuView(TemplateView):
    """
    Displays the lunch menu page.
    """
    template_name = 'bookings/lunch_menu.html'

class DinnerMenuView(TemplateView):
    """
    Displays the dinner menu page.
    """
    template_name = 'bookings/dinner_menu.html'