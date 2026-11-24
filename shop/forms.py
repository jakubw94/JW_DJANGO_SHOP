from django import forms
from utils import BootstrapFormMixin
from .models import Product
from django.db import transaction
from .models import ProductImage, Order


# Contact Form #
class ContactForm(BootstrapFormMixin, forms.Form):
    email = forms.EmailField(required=True, label="Email")
    subject = forms.CharField(required=True, min_length=5, max_length=200, label="Subject")
    message = forms.CharField(required=True, min_length=10, max_length=2000, label="Message",
                              widget=forms.Textarea(attrs={"rows": 5}))


# Order Form #
class MakeOrderForm(BootstrapFormMixin, forms.ModelForm):
    first_name = forms.CharField(required=True, min_length=3, max_length=50, label="First name")
    last_name = forms.CharField(required=True, min_length=3, max_length=50, label="Last name")
    email = forms.EmailField(required=True, max_length=100, label="Email")
    address_1 = forms.CharField(required=True, min_length=5, max_length=50, label="Streer and number")
    address_2 = forms.CharField(required=False, label="Apartment number (optional)")
    zip_code = forms.CharField(required=True, min_length=6, max_length=6, label="Zip-code")
    city = forms.CharField(required=True, min_length=3, label="City")
    phone = forms.CharField(required=True, min_length=9, max_length=12, label="Phone number")
    accept_terms = forms.BooleanField(required=True, label="I accept terms and conditions")

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address_1", "address_2", "zip_code", "city", "phone"]
