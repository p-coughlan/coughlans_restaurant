from django.db import models

# Create your models here.
from django.db import models

class Customer(models.Model):
    """
    Stores common customer details.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Booking(models.Model):
    """
    A model to store booking information.
    Each booking is linked to a Customer.
    """
    # Using SET_NULL so that if a customer is deleted, the booking remains (adjust as needed)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()

    def __str__(self):
        customer_name = self.customer.name if self.customer else "Anonymous"
        return f"{customer_name} - {self.date} at {self.time}"
