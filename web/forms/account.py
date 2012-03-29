from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=True)

class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=True)
    firstname = forms.CharField(max_length=100, required=True)
    lastname = forms.CharField(max_length=100, required=True)
    username = forms.CharField(max_length=100, required=True)
