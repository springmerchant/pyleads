from django.conf.urls.defaults import *
from django.contrib import admin
from pyleads.orders.models import *

info_dict = {
    'queryset': Buying.objects.all(),
}

admin.autodiscover()

urlpatterns = patterns('',
	 (r'^remote/addview/', 'pyleads.remote.views.index'),
	 (r'^remote/addclick/', 'pyleads.remote.views.addclick'),
	 (r'^remote/css/', 'pyleads.remote.views.formcss'),
	 (r'^remote/data/homebiz/1/', 'pyleads.data.views.homebiz_one'),
	 (r'^remote/data/homebiz/2/', 'pyleads.data.views.homebiz_two'),
	 (r'^remote/data/homebiz/3/', 'pyleads.data.views.homebiz_three'),
	 (r'^data/design/$', 'pyleads.data.views.designlead_final'),
         
	 (r'^publisher/register/$', 'pyleads.accounts.views.register', {'type':'publisher'}),
	 (r'^buyer/register/$', 'pyleads.accounts.views.register', {'type':'buyer'}),
	 (r'^panel/buyer/$', 'pyleads.profiles.views.buyer'),
	 (r'^publisher/$', 'pyleads.campaign.views.list_campaign'),	
	 (r'^publisher/balance/$', 'pyleads.profiles.views.publisher_balance'),	 
	 (r'^publisher/edit/$', 'pyleads.profiles.views.edit_profile_publisher'),
	 (r'^publisher/payment/$', 'pyleads.profiles.views.edit_payment'),
	 (r'^logout/$', 'pyleads.accounts.views.logout'),	
	 (r'^login/$', 'pyleads.accounts.views.do_login'),	
	 (r'^buyer/orders/buy/', 'pyleads.orders.views.buy_leads_main'),
	 (r'^buyer/orders/view/', 'pyleads.orders.views.view_leads'),
	 (r'^buyer/funds/', 'pyleads.orders.views.funds'),
	 (r'^buyer/ipn/', 'pyleads.orders.views.ipn'),
	 (r'^buyer/captured/(?P<order>\d{1,3})/$', 'pyleads.orders.views.captured_leads'),	 
	 (r'^buyer/edit/$', 'pyleads.profiles.views.edit_profile'),
	 (r'^buyer/$', 'pyleads.orders.views.control_panel'),
	 (r'^campaign/new/', 'pyleads.campaign.views.new_campaign'),
	 (r'campaign/edit/(?P<campaign>\d{1,3})/$','pyleads.campaign.views.edit_campaign'),
	 (r'campaign/delete/(?P<campaign>\d{1,3})/$','pyleads.campaign.views.delete_campaign'),
	 (r'campaign/tracker/edit/(?P<tracker>\d{1,3})/$','pyleads.campaign.views.edit_tracker'),
	 (r'campaign/tracker/stats/(?P<tracker>\d{1,3})/$','pyleads.campaign.views.stats_tracker'),
	 (r'campaign/tracker/add/(?P<campaignpk>\d{1,3})/$','pyleads.campaign.views.new_campaign'),
	 (r'campaign/list/$','pyleads.campaign.views.list_campaign'),
	 (r'campaign/detail/$','pyleads.campaign.views.list_campaign'),
	 (r'^javascript/(?P<type>\w+)/(?P<tracker>\w+)/$', 'pyleads.remote.views.javascript'),
	 (r'^testing/', 'django.views.generic.list_detail.object_list', info_dict),
	 (r'^$', 'pyleads.website.views.main'),
	 (r'^contact/$', 'pyleads.website.views.contact'),
	 (r'^about/$', 'pyleads.website.views.about'),
	 (r'^admin/(.*)', admin.site.root),
)
