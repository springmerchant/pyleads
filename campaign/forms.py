from django import forms 
from django.forms.widgets import Select
from django.template import Context, loader
from django.contrib.auth.models import User, Group
from pyleads.campaign.models import Campaign, Tracker, FormCss

class CampaignForm(forms.ModelForm):
#	CTYPE = (
#    ('homebiz', 'Home Business Leads'),)
#	campaign_type = forms.ChoiceField(choices=CTYPE)

    class Meta:
        model = Campaign
        fields = ['name','type']

class TrackerForm(forms.ModelForm):

    class Meta:
        model = Tracker
        fields = ('name',)

    def add_prefix(self, field_name):
        return self.prefix and ('%s_%s' % (self.prefix, field_name)) or field_name	

class DesignForm(forms.ModelForm):  

    def __init__(self, *args, **kwargs):
        super(DesignForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].widget.attrs = {'class':'small_input'}

    class Meta:
        model = FormCss
        exclude = ['tracker']

class StatDatesForm(forms.Form):
    POSSIBLE_DATES = (
        ('today', 'Today'),
        ('yesterday', 'Yesterday'),
        ('cur_month', 'This Month'),
        ('cur_year', 'This Year'),
        )
    dates = forms.ChoiceField(choices=POSSIBLE_DATES)