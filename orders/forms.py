from django import forms
from django.forms.widgets import Select

from pyleads.orders.models import Buying
from pyleads.orders.models import DepositAmount
from pyleads.profiles.models import UserProfile

class BuyingForm(forms.ModelForm):
	filter_zip = forms.IntegerField(required=False)
	
	CTYPE = (
				('homebiz', 'Home Business Leads'),
				('webdes', 'Web Design'),
	)
#	campaign_type = forms.ChoiceField(choices=CTYPE)
	type = forms.ChoiceField(choices=CTYPE)
	#def __init__(self, req, *args, **kwargs):
	#	super(BuyingForm, self).__init__(*args, **kwargs)
		
	def clean(self):
		q = self.cleaned_data.get('quantity')
		p = self.cleaned_data.get('price')
		
		if(q > 0 and p > 0):
			total = q  * p
			try:
				buyer_profile = self.instance.user.get_profile()
			except UserProfile.DoesNotExist:
				buyer_profile = UserProfile(user=self.instance.user,  balance=0)
				buyer_profile.save()
				
			if buyer_profile.balance < total:
				error = u'Not Enough Funds. Please add more funds to your account. You have %d dollars.' % buyer_profile.balance
				raise forms.ValidationError(error)
			else:
				buyer_profile.balance = buyer_profile.balance - total
				buyer_profile.save()

		return self.cleaned_data
		
	class Meta:
		model = Buying
		exclude = ('user','date')

class DepositForm(forms.ModelForm):
	
	def clean_amount(self):
		if self.cleaned_data.get('amount') < 0:
			raise forms.ValidationError("Please enter a positive number.")
		return self.cleaned_data.get('amount')
		
	class Meta:
		model = DepositAmount
		exclude = ('user','txn_id')