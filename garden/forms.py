from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User  
        fields = ['username', 'email', 'password1', 'password2'] 


class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['service_name', 'details', 'price']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'date', 'phone_number']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Set input type to 'date'
        }