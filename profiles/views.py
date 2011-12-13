# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from pyleads.campaign.models import Campaign
from pyleads.profiles.decorators import publisher_required, buyer_required

from pyleads.profiles.forms import EditProfileForm, EditPublisherForm, EditPaymentForm
from pyleads.profiles.models import UserProfile



@buyer_required
def edit_profile(request):
	user = request.user
	profile = user.get_profile()
	
	if request.method == "POST":
		form = EditProfileForm(data=request.POST, instance=profile)
		
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/buyer/edit/')
	else:
		form = EditProfileForm(instance=profile)
		
	return render_to_response('profiles/buyer/edit_profile.html', {'profile':form}, context_instance=RequestContext(request))
	
@publisher_required
def edit_profile_publisher(request):
	user = request.user
	
	try:
		profile = user.get_profile()
	except UserProfile.DoesNotExist:
		profile = UserProfile(user=user,  balance=0)
		profile.save()
	
	if request.method == "POST":
		form = EditPublisherForm(data=request.POST, instance=profile)
		
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/publisher/edit/')
	else:
		form = EditPublisherForm(instance=profile)
		
	return render_to_response('profiles/seller/edit_profile.html', {'profile':form}, context_instance=RequestContext(request))

@publisher_required
def edit_payment(request):
	user = request.user
	
	profile, created = UserProfile.objects.get_or_create(user=user)
	
	if request.method == "POST":
		form = EditPaymentForm(data=request.POST, instance=profile)
		
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/publisher/')
	else:
		form = EditPaymentForm(instance=profile)
		
	return render_to_response('profiles/seller/edit_payment.html', {'profile':form}, context_instance=RequestContext(request))

@publisher_required
def publisher_balance(request):
	user = request.user
	
	profile, created = UserProfile.objects.get_or_create(user=user)
		
	return render_to_response('profiles/seller/balance.html', {'profile':profile}, context_instance=RequestContext(request))	
	

@login_required
def buyer(request):
	user = request.user
	
	if user.groups.filter(name='buyer').count() >  0:
		return HttpResponse("Create New Campaign<br />Edit Campaign")
	else:
		return HttpResponse("You are not a buyer")

@publisher_required	
def publisher(request):
	user = request.user
	errors = []
	
	try:
		camps = Campaign.objects.filter(user=user);
	except Campaign.DoesNotExist:
		errors.insert(0,'You do not have a campaign')
	
	for c in camps:
		if c.clicks and c.impressions > 0:
			c.ctr = round((float(c.clicks)/c.impressions * 100), 2)

	return render_to_response('profiles/seller/main.html', {'campaigns':camps,'errors': errors}, context_instance=RequestContext(request))

def buyer(request):
	user = request.user
	
	return render_to_response('profiles/buyer/main.html', context_instance=RequestContext(request))
	