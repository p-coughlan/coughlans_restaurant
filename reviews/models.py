from django.db import models

# Import the Customer model from the bookings app
from bookings.models import Customer 

# Create your models here.
class Review(models.Model):
    """
    A model to store customer reviews.
    Each review may be linked to a Customer if provided.
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Rating out of 5
    approved = models.BooleanField(default=False)    # Only approved reviews are displayed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.customer:
            return f"Review by {self.customer.name} ({'Approved' if self.approved else 'Pending'})"
        return f"Anonymous Review ({'Approved' if self.approved else 'Pending'})"