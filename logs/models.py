from django.db import models
from django.contrib.auth.models import User

from pyleads.campaign.models import Tracker
from pyleads.orders.models import Buying

class TrackerLog(models.Model):
	tracker = models.ForeignKey(Tracker)
	impressions = models.IntegerField(blank=True, default=0, null=True)
	clicks = models.IntegerField(blank=True, default=0, null=True)
	leads_total = models.IntegerField(blank=True, default=0, null=True)
	leads_sold = models.IntegerField(blank=True, default=0, null=True)
	sold_total = models.DecimalField(max_digits=5, decimal_places=2)
	date = models.DateField(blank=True, null=True)
	
class UserLog(models.Model):
	user = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=5, decimal_places=2)


from pyleads.data.models import BaseLead, DesignLead

class LeadLog(models.Model):
	order = models.ForeignKey(Buying)
	lead = models.ForeignKey(DesignLead)
	date = models.DateTimeField()
	
	def __unicode__(self):
		return "hi"
	
	class Admin:
		pass