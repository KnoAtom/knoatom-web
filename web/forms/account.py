from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=102, required=True)
    redirect = forms.CharField(widget=forms.widgets.HiddenInput, required=False)

class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=100, required=True, label='First Name')
    lastname = forms.CharField(max_length=100, required=True, label='Last Name')
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=True)

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, max_length=100, required=True)
