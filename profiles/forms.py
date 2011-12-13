from django import forms
from django.forms.widgets import Select

from pyleads.orders.models import Buying
from pyleads.orders.models import DepositAmount
from pyleads.profiles.models import UserProfile

class EditProfileForm(forms.ModelForm):
		
	class Meta:
		model = UserProfile
		exclude = ('user','balance')
		
class EditPaymentForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		exclude = ('user','balance','address','city','phone','state','zipcode','country')
		
class EditPublisherForm(forms.ModelForm):
		
	class Meta:
		model = UserProfile
		exclude = ('user','balance')