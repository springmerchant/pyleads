from datetime import datetime
import decimal
import urllib
import urllib2

from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.paginator import Paginator

from pyleads.profiles.decorators import buyer_required
from pyleads.profiles.models import UserProfile
from pyleads.logs.models import UserLog
from pyleads.orders.forms import BuyingForm, DepositForm
from pyleads.orders.models import Buying, DepositAmount
from pyleads.logs.models import LeadLog

@buyer_required	
def buy_leads_main(request):
	user = request.user		
	
	open_orders=Buying.objects.filter(type='homebiz', open='1')
	
	orders = 0
	leads = 0
	total = decimal.Decimal("0")
	highest = decimal.Decimal("0")
	average = decimal.Decimal("0")
			
	for open_order in open_orders:
		orders=orders+1
		total = total + open_order.price
		leads = leads + open_order.quantity
			
		if open_order.price > highest:
			highest = open_order.price
	
	if total > 0:

		average = round((total/orders),2)
		
	stats = {'orders':orders, 'avg':average, 'lead_quantity':leads, 'highest_price':highest}
	
	if request.method == 'POST':	
		buying = Buying(user=request.user)
		buying.date = datetime.today()
		buying_form = BuyingForm(data=request.POST, instance=buying)	

		if buying_form.is_valid():		
			buying_form.save()
			
			return render_to_response('campaign/buyer/done.html', {'order':buying_form},context_instance=RequestContext(request))
	else:

		buying_form = BuyingForm()
		
	return render_to_response('campaign/buyer/form.html', {'form':buying_form, 'stats':stats},context_instance=RequestContext(request))

@buyer_required
def view_leads(request):
	user = request.user
	
	orders = Buying.objects.filter(user=user)

	return render_to_response('campaign/buyer/list.html', {'orders':orders}, context_instance=RequestContext(request))

@buyer_required
def captured_leads(request, order):
	user = request.user
	
	order = get_object_or_404(Buying, pk=order)
	
	if order.user == user:
		leads = LeadLog.objects.filter(order=order)
		
		for l in leads:
			l.lead.sold_at = round(l.lead.sold_at / decimal.Decimal(".8"),2)

		return render_to_response('campaign/buyer/captured_detail.html', {'leads':leads, 'order':order}, context_instance=RequestContext(request))

@buyer_required
def control_panel(request):
	return render_to_response('campaign/buyer/main.html', {}, context_instance=RequestContext(request))
	
@buyer_required
def funds(request):
	if request.method == 'POST':
		deposit_form = DepositForm(data=request.POST)
		
		if deposit_form.is_valid():
			deposit = deposit_form.save(commit=False)
			deposit.user = request.user
			deposit.save()
		
			url = 'https://www.paypal.com/cgi-bin/webscr?cmd=_xclick'
			currency = 'USD'
			amount = request.POST.get('amount')
			item_name = 'Pyleads Deposit'
			custom = deposit.pk
				
			return HttpResponseRedirect("%s&business=%s&item_name=%s&item_number=1\
			&amount=%s&no_shipping=0&no_note=1&currency_code=%s&custom=%s\
			&notify_url=%s&return=%s&lc=US&bn=PP-BuyNowBF&charset=UTF-8" % (url, 'emilian@felecan.com', item_name,\
			amount, currency, custom, '', ''))
	else:
		deposit_form = DepositForm()
		
	return render_to_response('campaign/buyer/funds.html', {'form':deposit_form}, context_instance=RequestContext(request))

def ipn(request):
	PP_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
	parameters = request.POST.copy()
	parameters['cmd']='_notify-validate'
	params = urllib.urlencode(parameters)
	req = urllib2.Request(PP_URL, params)
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	response = urllib2.urlopen(req)
	status = response.read()
	
	if status == "VERIFIED":
		deposit = DepositAmount.objects.get(pk=parameters['custom'])
		deposit.txn_id = parameters['txn_id']
		deposit.save()
		
		# Add balance to user
		profile = UserProfile.objects.get(user=deposit.user)
		profile.balance = profile.balance + deposit.amount
		
		# Add log
		userlog = UserLog(user=deposit.user, amount=deposit.amount)
		userlog.save()
		
		return HttpResponse('d')
	return HttpResponse(status)
		
	