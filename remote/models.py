from django.db import models
from pyleads.logs.models import TrackerLog
	
# Create your models here.
class LeadView(models.Model):
	trackerlog = models.ForeignKey(TrackerLog) 
	url =  models.CharField(max_length=255) 
	time = models.DateTimeField()