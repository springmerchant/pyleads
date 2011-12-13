from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	balance = models.DecimalField(max_digits=6, decimal_places=2)
	address = models.CharField(max_length=256)
	city = models.CharField(max_length=256)
	state = models.CharField(max_length=32)
	country = models.CharField(max_length=2)
	zipcode = models.CharField(max_length=12)
	phone = models.CharField(max_length=32)
	paypal = models.EmailField()
	
	def __unicode__(self):
		return "%s's Profile" % self.user.username
		
	class Admin:
		pass
