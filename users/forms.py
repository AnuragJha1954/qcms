from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "phone",
            "store_name",
            "password1",
            "password2",
        ]