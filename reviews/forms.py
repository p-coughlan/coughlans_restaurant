from django import forms
from .models import Review
from bookings.models import Customer  # Ensure the Customer model is imported

class ReviewForm(forms.ModelForm):
    """
    Form for submitting a review.
    
    This form collects the review's comment and a rating using a star-based input.
    Additional customer details are optional and used to link the review to a Customer.
    """
    customer_name = forms.CharField(max_length=100, label="Your Full Name", required=False,
                                    help_text="")
    customer_email = forms.EmailField(label="Your Email", required=False,
                                      help_text="")
    customer_phone = forms.CharField(max_length=15, label="Your Phone Number", required=False,
                                     help_text="")
    
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rating': forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)], #how to not dispaly the numbers - use a star image instead - 
                attrs={'class': 'radiolist rating'}  # Add both classes
            ),
        }
        help_texts = {
            'comment': "Write your review here.",
            'rating': "",
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize the form and set the default rating to 5."""
        super().__init__(*args, **kwargs)
        self.fields['rating'].initial = 5
    
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