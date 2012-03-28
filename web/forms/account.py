from django import forms

class LoginForm(forms.Form):
    email = forms.charField(max_length=100)
    password = forms.charField(max_length=100)
