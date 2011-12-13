import md5, random, decimal
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils import simplejson
from django.db.models import Q

from pyleads.data.models import BaseLead, DesignLead
from pyleads.orders.models import Buying
from pyleads.campaign.models import Campaign, Tracker, FormCss
from pyleads.profiles.models import UserProfile
from pyleads.logs.models import UserLog, TrackerLog, LeadLog


def homebiz_one(request):
	us_state = request.GET.get('state')
	phone = '123-123-3492'
	
	if not request.GET.has_key('callback'):
		return HttpResponse('Please provide a callback function.')
		
	if not us_state:
		return HttpResponse('Please provide a state.')
		
	try:
		tracker_log = TrackerLog.objects.get(date=datetime.today(), tracker__name=request.GET.get('tracker'))
	except TrackerLog.DoesNotExist:
		return HttpResponse("Invalid tracker.")
		
	lead = BaseLead(leadid=md5.new(str(random.random())).hexdigest(), trackerlog=tracker_log, state=us_state, phone=phone, rent_own=1, reach_time=1, sold_at=0)
	lead.save()
	
	json = simplejson.dumps({"leadid":lead.leadid, "tracker":tracker_log.tracker.name});
	
	return HttpResponse(request.GET['callback']+'('+json+')')

def homebiz_two(request):	
	try:
		lead = BaseLead.objects.get(leadid=request.GET['leadid'])
	except BaseLead.DoesNotExist:
		return HttpResponse("Lead id does not exist.")
	
	lead.first_name = request.GET['firstname']
	lead.last_name = request.GET['lastname']
	lead.email = request.GET['email']
	lead.phone = request.GET['phone1'] + '-' + request.GET['phone2'] + '-' + request.GET['phone3']
	lead.zip = request.GET['zipcode']
	
	lead.save()
	
	# dictionary
	return_dict =	{
						'leadid': request.GET['leadid'],
						'tracker': request.GET.get('tracker'),
					}
	
	json = simplejson.dumps(return_dict)
	
	return HttpResponse(request.GET['callback']+'('+json+')')

def homebiz_three(request):
	try:
		lead = BaseLead.objects.get(leadid=request.GET['leadid'])
	except BaseLead.DoesNotExist:
		return HttpResponse("Lead id does not exist.")
	
	lead.rent_own = request.GET['rentown']
	lead.reach_time = request.GET['reachtime']
	lead.address = request.GET['address']
	lead.city = request.GET['city']
	
	lead.save()
	
	tracker = lead.trackerlog.tracker
	campaign = tracker.campaign
	
	lead.trackerlog.leads_total = lead.trackerlog.leads_total + 1
	lead.trackerlog.save()
	
	campaign.leads_total = campaign.leads_total + 1
	campaign.save()
	
	try:
		buying = Buying.objects.all().filter(type__iexact='homebiz').filter(Q(filter_state__iexact=lead.state) | Q(filter_state__iexact='*') | Q(filter_zip__iexact=lead.zip)).order_by('-price')[0:1].get()
	except Buying.DoesNotExist:
		return HttpResponse("No buyers found.")
		
	if buying is not None:
		buying.quantity = buying.quantity-1
		buying.save()	
		
		try:
			buyer_profile = buying.user.get_profile()
		except UserProfile.DoesNotExist:
			buyer_profile = UserProfile(user=buying.user,  balance=0)
			buyer_profile.save()
			
		publisher_price = buying.price * decimal.Decimal(".8")
		our_price = buying.price * decimal.Decimal(".2")
		
		if buyer_profile.balance < buying.price:
			return HttpResponse("Could not commplete transaction. Not enough balance.")
		else:
			buyer_profile.balance -= buying.price
			buyer_profile.save()
			
			try:
				publisher_profile = campaign.user.get_profile()
			except UserProfile.DoesNotExist:
				publisher_profile = UserProfile(user=campaign.user, balance=0)
				publisher_profile.save()
				
			publisher_profile.balance += publisher_price
			publisher_profile.save()
			
			lead.trackerlog.leads_sold +=  1
			lead.trackerlog.sold_total += publisher_price
			lead.trackerlog.save()
		
			campaign.leads_sold += 1
			campaign.save()
			
			lead.sold_at = publisher_price
			lead.save()
			
			publisher_log = UserLog(user=campaign.user, amount=publisher_price)
			publisher_log.save()

			buyer_log = UserLog(user=buying.user, amount=-(publisher_price+our_price))
			buyer_log.save()
			
			buyer_lead_log = LeadLog(order=buying, lead=lead, date=datetime.today())
			buyer_lead_log.save()
			
			our_log = UserLog(user=User.objects.get(pk=1), amount=our_price)
			our_log.save()
			
			our_log.user.get_profile().balance += our_price
			our_log.user.get_profile().save()
			
	return_dict = {
					'location': buying.location,
					'leadid': request.GET['leadid'],
				}
	
	json = simplejson.dumps(return_dict)
	
	return HttpResponse(request.GET['callback']+'('+json+')')

def designlead_final(request):
	try:
		tracker_log = TrackerLog.objects.get(date=datetime.today(), tracker__name=request.GET.get('tracker'))
	except TrackerLog.DoesNotExist:
		return HttpResponse("Invalid tracker.")
	
	phone = request.GET.get('phone')
	description = request.GET.get('description')
	budget = request.GET.get('budget')
	first_name = request.GET.get('first_name')
	last_name = request.GET.get('last_name')
	
	lead = DesignLead(leadid=md5.new(str(random.random())).hexdigest(), trackerlog=tracker_log, phone=phone,
				last_name=last_name, first_name=first_name, budget=budget, description=description, sold_at=0)
	lead.save()
	
	tracker = lead.trackerlog.tracker
	campaign = tracker.campaign
	
	lead.trackerlog.leads_total = lead.trackerlog.leads_total + 1
	lead.trackerlog.save()
	
	campaign.leads_total = campaign.leads_total + 1
	campaign.save()
	
	try:
		buying = Buying.objects.filter(type__id='1').order_by('-price')[0:1].get()
	except Buying.DoesNotExist:
		return HttpResponse("No Buyers")
		
	if buying is not None:
		buying.quantity = buying.quantity-1
		buying.save()	
		
		try:
			buyer_profile = buying.user.get_profile()
		except UserProfile.DoesNotExist:
			buyer_profile = UserProfile(user=buying.user,  balance=0)
			buyer_profile.save()
			
		publisher_price = buying.price * decimal.Decimal(".8")
		our_price = buying.price * decimal.Decimal(".2")
		
		if buyer_profile.balance < buying.price:
			return HttpResponse("Could not commplete transaction. Not enough balance.")
		else:
			buyer_profile.balance -= buying.price
			buyer_profile.save()
			
			try:
				publisher_profile = campaign.user.get_profile()
			except UserProfile.DoesNotExist:
				publisher_profile = UserProfile(user=campaign.user, balance=0)
				publisher_profile.save()
				
			publisher_profile.balance += publisher_price
			publisher_profile.save()
			
			lead.trackerlog.leads_sold +=  1
			lead.trackerlog.sold_total += publisher_price
			lead.trackerlog.save()
		
			campaign.leads_sold += 1
			campaign.save()
			
			lead.sold_at = publisher_price
			lead.save()
			
			publisher_log = UserLog(user=campaign.user, amount=publisher_price)
			publisher_log.save()

			buyer_log = UserLog(user=buying.user, amount=-(publisher_price+our_price))
			buyer_log.save()
			
			buyer_lead_log = LeadLog(order=buying, lead=lead, date=datetime.today())
			buyer_lead_log.save()
			
			our_log = UserLog(user=User.objects.get(pk=1), amount=our_price)
			our_log.save()
			
			our_log.user.get_profile().balance += our_price
			our_log.user.get_profile().save()
		
	return_dict = {
					'location': buying.location,
					'leadid': lead.leadid,
				}
	
	json = simplejson.dumps(return_dict)
	
	return HttpResponse(request.GET['callback']+'('+json+')', mimetype='application/json'))
	
