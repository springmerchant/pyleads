from django.db import models
from pyleads.logs.models import TrackerLog
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField
"""
class BaseLead(models.Model):
	leadid = models.CharField(max_length=32)
	trackerlog = models.ForeignKey(TrackerLog)
	last_name = models.CharField(max_length=255)
	first_name = models.CharField(max_length=255)
	phone = PhoneNumberField()
	address = models.CharField(max_length=255)
	state = USStateField()
	email = models.EmailField()
	city = models.CharField(max_length=128)
	rent_own = models.PositiveSmallIntegerField(blank=True)
	reach_time = models.PositiveSmallIntegerField(blank=True)
	zip = models.CharField(max_length=12)
	sold_at = models.DecimalField(max_digits=5, decimal_places=2)
        """
class BaseLead(models.Model):
	leadid = models.CharField(max_length=32)
	trackerlog = models.ForeignKey(TrackerLog)
	sold_at = models.DecimalField(max_digits=5, decimal_places=2)
	
	
class DesignLead(BaseLead):
	last_name = models.CharField(max_length=255)
	first_name = models.CharField(max_length=255)
	email = models.EmailField()
	phone = PhoneNumberField()
	budget = models.DecimalField(max_digits=5, decimal_places=2)
	description = models.CharField(max_length=255)