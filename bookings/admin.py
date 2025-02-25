from django.contrib import admin
# Import Customer and Booking models
from .models import Customer, Booking

# Register your models here.
admin.site.register(Customer) # Register Customer model
admin.site.register(Booking) # Register Booking model

