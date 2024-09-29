from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomerUser, Stack


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ['username', 'first_name', 'image','last_name', 'gender', 'email', 'country', 'phone_number']



class AddStackForm(forms.ModelForm):
    class Meta:
        model = Stack
        fields = ['title', 'assigned_to', 'status', 'duration', 'image', 'description',]


