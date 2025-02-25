# reviews/forms.py

from django import forms
from .models import Review
from bookings.models import Customer  # Import Customer from bookings app

class ReviewForm(forms.ModelForm):
    """
    Form for submitting a review. Optionally links a review to a Customer.
    """
    customer_name = forms.CharField(max_length=100, label="Your Name", required=False)
    customer_email = forms.EmailField(label="Your Email", required=False)
    customer_phone = forms.CharField(max_length=15, label="Your Phone", required=False)
    
    class Meta:
        model = Review
        # Only review-specific fields are included here.
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def save(self, commit=True):
        review = super().save(commit=False)
        email = self.cleaned_data.get('customer_email')
        name = self.cleaned_data.get('customer_name')
        phone = self.cleaned_data.get('customer_phone')
        if email:
            customer, created = Customer.objects.get_or_create(
                email=email,
                defaults={'name': name if name else "Anonymous", 'phone': phone}
            )
            review.customer = customer
        if commit:
            review.save()
        return review
