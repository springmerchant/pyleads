from django.db import models
from django.contrib.auth.models import User


class Type(models.Model):
	name = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.name

class Campaign(models.Model):
	cid = models.AutoField(primary_key=True)
	user = models.ForeignKey(User)
	type = models.ForeignKey(Type)
	name = models.CharField(max_length=255)
	impressions = models.IntegerField(blank=True, default=0, null=True)
	clicks = models.PositiveIntegerField(blank=True, default=0, null=True)
	leads_total = models.PositiveIntegerField(blank=True, default=0, null=True)
	leads_sold = models.PositiveIntegerField(blank=True, default=0, null=True)
	
STYLE_CHOICES = (	
	('solid', 'Solid'),
    ('dashed', 'Dashed'),
    ('dotted', 'Dotted'),
)	

class FormCss(models.Model):
	border_color = models.CharField(max_length=16, default='#000000')
	border_width = models.CharField(max_length=16, default='1')
	border_style = models.CharField("border Style", max_length=16, choices=STYLE_CHOICES, default='solid')
	bg_color = models.CharField("background color", max_length=16, default='#ffffff')
	font_color = models.CharField(max_length=16, default='#000000')	
	input_bg_color = models.CharField(max_length=16, default='#ffffff')
	input_color = models.CharField(max_length=16, default='#000000')

class Tracker(models.Model):
	tid = models.AutoField(primary_key=True)
	campaign = models.ForeignKey(Campaign)
	name = models.CharField(max_length=255)
	design = models.ForeignKey(FormCss)
	

	


