from django import forms
from .models import Account


class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = Account
        fields = ('name', 'email', 'password')
