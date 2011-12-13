from django import forms
from django.template import Context, loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

class UserForm(forms.Form):
	email = forms.EmailField(max_length=255, min_length=6)
	username = forms.CharField(max_length=255, min_length=3)
	password1 = forms.CharField( min_length=6, widget=forms.PasswordInput )
	password2 = forms.CharField( min_length=6, widget=forms.PasswordInput )
	
	def clean_username(self):
		if len(User.objects.filter(username=self.cleaned_data.get("username"))) == 0:
			return self.cleaned_data.get("username")
		else:
			raise forms.ValidationError("The username is already registered.")
			
	def clean_password2(self):
		if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
			raise forms.ValidationError("The passwords do not match")

class LoginForm(forms.Form):
	TEST = (
    ('publisher', 'Lead Publisher'),
    ('buyer', 'Lead Buyer'))
	
	username = forms.CharField(max_length=255, min_length=5)
	password = forms.CharField(max_length=255, min_length=6, widget=forms.PasswordInput)
	group = forms.ChoiceField(choices=TEST)
	