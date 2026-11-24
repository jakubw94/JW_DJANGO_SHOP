from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserInfo
from utils import BootstrapFormMixin
from django.db import transaction


# Modified default user creation form -> email as username + UserInfo 1:1 model fields #
class RegisterForm(BootstrapFormMixin, UserCreationForm):
    # User model fields #
    username = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, min_length=3, max_length=50, label="First name")
    last_name = forms.CharField(required=True, min_length=3, max_length=50, label="Last name")
    # UserInfo model fields #
    address_1 = forms.CharField(required=True, label="Street and number")
    address_2 = forms.CharField(required=False, label="Apartment number (optional)")
    zip_code = forms.CharField(required=True, min_length=6, max_length=6, label="Zip-code")
    city = forms.CharField(required=True, label="City")
    phone = forms.CharField(required=True, min_length=9, max_length=12, label="Phone number")
    # Accept terms field #
    accept_terms = forms.BooleanField(required=True, label="I accept terms and conditions")

    # Defining fields from User model #
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]

    # Rewriting save method #
    def save(self, commit=True):
        # Creating User #
        user = super().save(commit=False)
        user.email = user.username
        if commit:
            with transaction.atomic():
                user.save()
                # Creating UserInfo #
                user_info = {"user": user,
                             "address_1": self.cleaned_data["address_1"],
                             "address_2": self.cleaned_data["address_2"],
                             "zip_code": self.cleaned_data["zip_code"],
                             "city": self.cleaned_data["city"],
                             "phone": self.cleaned_data["phone"]}
                UserInfo.objects.create(**user_info)
        return user


### Change user delivery data Form ###
class ChangeDeliveryDataForm(forms.ModelForm):
    address_1 = forms.CharField(max_length=50)
    address_2 = forms.CharField(max_length=50, required=False)
    zip_code = forms.CharField(min_length=6, max_length=6, label='Zip-Code')
    city = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = UserInfo
        fields = ['address_1' ,'address_2', 'zip_code', 'city', 'phone']