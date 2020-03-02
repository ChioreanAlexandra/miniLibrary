from django import forms
from django.forms.utils import ErrorList
class UploadFileForm(forms.Form):
    file = forms.ImageField()

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=200)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())

class UserForm(forms.Form):
    username = forms.CharField(label='Username',max_length=200)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    password_match = forms.CharField(label='Password',widget=forms.PasswordInput())
   