# bookings/forms.py
from datetime import time
from django import forms
from .models import Booking, Customer
from bookings.models import Customer  # Ensure the Customer model is imported

# The form includes additional fields (customer_name, customer_email, and customer_phone) to capture customer details, which are then used in the save() method to either retrieve or create a Customer instance.
class BookingForm(forms.ModelForm):
    """
    Form for creating a booking. Collects customer details and booking-specific details.
    Creates or retrieves a Customer based on the provided email.

    Validations:
      - The number of guests must be at least 1.
      - The booking time must fall within the restaurant's operating hours:
          Lunch: 11:00 AM - 3:00 PM
          Dinner: 5:00 PM - 9:00 PM

    """
    customer_name = forms.CharField(max_length=100, label="Your Name")
    customer_email = forms.EmailField(label="Your Email")
    customer_phone = forms.CharField(max_length=15, label="Your Phone")

    date = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'dd-mm-yyyy', 'type': 'text'}),
        input_formats=['%d-%m-%Y'],
    )
    time = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'placeholder': 'HH:MM', 'type': 'text'}),
        input_formats=['%H:%M'],
    )

    # The Meta class specifies that only date, time, and guests are directly handled as booking-specific fields. Customer information is handled separately.
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests']
        help_texts = {
            'date': 'Enter the booking date in dd-mm-yyyy format (e.g. 05-08-2025).',
            'time': 'Enter the booking time in HH:MM format (e.g. 18:00).',
        }

    def clean(self):
        cleaned_data = super().clean()
        booking_time = cleaned_data.get('time')
        guests = cleaned_data.get('guests')

        # Ensure at least one guest is booked.
        if guests is not None and guests < 1:
            self.add_error('guests', 'Please enter at least 1 guest.')

        # Validate the booking time is within operating hours.
        if booking_time:
            lunch_open = time(11, 0)
            lunch_close = time(15, 0)
            dinner_open = time(17, 0)
            dinner_close = time(21, 0)
            if not ((lunch_open <= booking_time <= lunch_close) or (dinner_open <= booking_time <= dinner_close)):
                self.add_error('time', 'Please select a time within our operating hours: 11:00-15:00 for lunch or 17:00-21:00 for dinner.')

        return cleaned_data

    def save(self, commit=True):
        # Create or retrieve the Customer using provided details.
        customer, created = Customer.objects.get_or_create(
            email=self.cleaned_data['customer_email'],
            defaults={
                'name': self.cleaned_data['customer_name'],
                'phone': self.cleaned_data['customer_phone'],
            }
        )
        booking = super().save(commit=False)
        booking.customer = customer
        if commit:
            booking.save()
        return booking

class AdminBookingForm(forms.ModelForm):
    """
    Form for admin/staff to update a booking.
    Excludes customer details (name, email, phone) so that staff can quickly modify
    the booking (e.g., change the number of guests or reschedule) without re-entering
    customer information.
    """
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests']
        help_texts = {
            'date': 'Enter the booking date in dd-mm-yyyy format (e.g. 05-08-2025).',
            'time': 'Enter the booking time in HH:MM format (e.g. 18:00).',
        }