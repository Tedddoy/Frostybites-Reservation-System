from django import forms
from .models import User
from .models import Services
from .models import Reservation


class CustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['service_name', 'details', 'price']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'date', 'phone_number',]          
