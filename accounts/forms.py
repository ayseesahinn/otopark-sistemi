from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

from .models import Parking, Reservation, CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = ['name', 'location', 'total_spots', 'available_spots', 'price_per_hour', 'description']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reserved_time', 'spots_reserved']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        
