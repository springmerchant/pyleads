from django.db import models
from django.contrib.auth.models import User

from pyleads.profiles.models import UserProfile
from pyleads.campaign.models import Type

STATE_CHOICES = (
    ('IL', 'Illinois'),
    ('FL', 'Florida'),
    ('CA', 'California'),
    ('*', 'All States'),
)

class Buying(models.Model):
	user = models.ForeignKey(User)
	type = models.ForeignKey(Type)
	price = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Price Per Lead")
	quantity = models.PositiveIntegerField(verbose_name="Number of Leads")
	post = models.PositiveSmallIntegerField()
	location = models.CharField(max_length=255, verbose_name="Send To (URL):")
	open = models.BooleanField(verbose_name="Open Order")
	date = models.DateTimeField()
	filter_state = models.CharField(max_length=2, choices=STATE_CHOICES)
	filter_zip = models.PositiveIntegerField(null=True)

	def __unicode__(self):
		return "%s's Buying Order" % self.user.username
	class Admin:
		pass
		
class DepositAmount(models.Model):
	user = models.ForeignKey(User)
	amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Amount To Deposit")
	txn_id = models.CharField(max_length=255)