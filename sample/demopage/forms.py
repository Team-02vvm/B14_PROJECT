# demopage/forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        # Check if the password field is left blank
        if not password:
            raise ValidationError('Password is required. Please enter a password.')

        # Custom password validation
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one number.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')

        return password

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')

        # Ensure password confirmation matches
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')

        # Check if the confirmation field is left blank
        if not password2:
            raise ValidationError('Password confirmation is required.')

        return password2

