# bookings/forms.py

from django import forms
from .models import Booking, Customer

class BookingForm(forms.ModelForm):
    """
    Form for creating a booking. Collects customer details and booking-specific details.
    Creates or retrieves a Customer based on the provided email.
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

    class Meta:
        model = Booking
        # Only Booking-specific fields are included here.
        fields = ['date', 'time', 'guests']
        help_texts = {
            'date': 'Enter the booking date in dd-mm-yyyy format (e.g. 05-08-2025).',
            'time': 'Enter the booking time in HH:MM format (e.g. 18:00).',
        }

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