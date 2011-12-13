# Create your views here.
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from pyleads.campaign.forms import CampaignForm, TrackerForm, DesignForm, StatDatesForm
from pyleads.campaign.models import Campaign, Tracker, FormCss
from pyleads.logs.models import TrackerLog
from pyleads.profiles.decorators import publisher_required
from django.template import RequestContext

from datetime import datetime

@publisher_required
def new_campaign(request, campaignpk=""):

    if campaignpk:
        campaign = Campaign.objects.get(pk=campaignpk)
        action = '/campaign/tracker/add/'+campaignpk+'/'
        button = 'Add Tracker'
        header = 'Add Tracker To Campaign'
    else:
        campaign = Campaign(user=request.user, impressions=0, clicks=0, leads_total=0, leads_sold=0)
        action = '/campaign/new/'
        button = 'Add Campaign'
        header = 'Add A New Campaign'

    design = FormCss()
    tracker = Tracker()

    if request.method == 'POST':
        campaign_form = CampaignForm(data=request.POST, instance=campaign)
        tracker_form = TrackerForm(data=request.POST, instance=tracker, prefix='t')
        design_form = DesignForm(data=request.POST, instance=design)

        if campaign_form.is_valid() and tracker_form.is_valid() and design_form.is_valid():
            c = campaign_form.save(commit=False)
            c.save()

            d = design_form.save(commit=False)
            d.save()	

            t = tracker_form.save(commit=False)
            t.campaign = c
            t.design = d
            t.save()

            tracker_log = TrackerLog(tracker=t)
            tracker_log.date = datetime.today()
            tracker_log.sold_total = 0
            tracker_log.save()

            return render_to_response('campaign/new_done.html', {'tracker':t}, context_instance=RequestContext(request))
        else:
            return render_to_response('campaign/new.html', {'campaign_form':campaign_form, 'design_form':design_form,
                                                            'tracker_form':tracker_form, 'action': action, 
                                                            'button':button, 'header':header},
                                                            context_instance=RequestContext(request))
    else:
        campaign_form = CampaignForm( instance=campaign)
        tracker_form = TrackerForm(instance=tracker, prefix='t')
        design_form = DesignForm(instance=design)

        return render_to_response('campaign/new.html', {'campaign_form':campaign_form,
                                                        'design_form':design_form, 'tracker_form':tracker_form,
                                                        'action': action, 'button':button, 'header':header},
                                                        context_instance=RequestContext(request))

@publisher_required
def edit_campaign(request, campaign):
    cx = Campaign.objects.get(pk=campaign)

    return render_to_response('campaign/edit.html', {'c':cx}, context_instance=RequestContext(request))

@publisher_required
def delete_campaign(request, campaign):
    c = Campaign.objects.get(pk=campaign)
    c.delete()

    return HttpResponseRedirect('/campaign/list/')

@publisher_required
def edit_tracker(request, tracker):
    try:
        t = Tracker.objects.get(pk=tracker)
    except Tracker.DoesNotExist:
        return HttpResponse("Tracker is invalid.")

    try:
        form = FormCss.objects.get(tracker=t)
    except FormCss.DoesNotExist:
        return HttpResponse("Form is not valid.")

    if request.POST:
        design = DesignForm(data=request.POST, instance=form)
        tracker_form = TrackerForm(data=request.POST, instance=t, prefix='t')
        campaign_form = CampaignForm(data=request.POST, instance=t.campaign)

        if design.is_valid() and tracker_form.is_valid() and campaign_form.is_valid():
            design.save()
            tracker_form.save()
            campaign_form.save()

            return HttpResponseRedirect("/campaign/list/")
    else:
        design = DesignForm(instance=form)
        tracker_form = TrackerForm(instance=t, prefix='t')
        campaign_form = CampaignForm(instance=t.campaign)

    return render_to_response('campaign/edit_tracker.html', {'design_form':design, 
                                                             'campaign_form':campaign_form, 
                                                             'tracker_form':tracker_form}, 
                                                             context_instance=RequestContext(request))

@publisher_required
def stats_tracker(request, tracker):
    user = request.user

    t = get_object_or_404(Tracker, pk=tracker)

    if t.campaign.user == user:
        trackers = TrackerLog.objects.filter(tracker=t).order_by('-date')

        return render_to_response('campaign/stats_tracker.html', {'trackers':trackers}, 
                                  context_instance=RequestContext(request))


@publisher_required
def list_campaign(request):
    user = request.user
    errors = []


    try:
        camps = Campaign.objects.filter(user=user)
    except Campaign.DoesNotExist:
        errors.insert(0,'You do not have a campaign')
        
    if request.GET.get('dates'):    
        stat_dates = StatDatesForm(request.GET)
        # calculate the totals
        if stat_dates.is_valid():
            type = stat_dates.cleaned_data.get('dates')
            d = datetime.today()
            
            if type == "today": 
                tracker_logs = TrackerLogs.objects.filter(date__day=d.day)
            elif type == "yesterday":
                tracker_logs = TrackerLogs.objects.filter(date__day=d.day-1)
            elif type == "cur_month":
                tracker_logs = TrackerLogs.objects.filter(date__month=d.month)
            elif type == "cur_year":
                tracker_logs = TrackerLogs.objects.filter(date__year=d.year)
            else:
                pass
    else:
        stat_dates = StatDatesForm()
        
    for c in camps:
        if c.clicks and c.impressions > 0:
            c.ctr = round((float(c.clicks)/c.impressions * 100), 2)

    return render_to_response('campaign/list.html', {'campaigns':camps,'errors': errors,'stat_dates':stat_dates}, 
                              context_instance=RequestContext(request))

@publisher_required
def profile(request):
    profile = request.user.get_profile()

    return render_to_response('accounts/publisher/profile.html', {'profile':profile}, 
                              context_instance=RequestContext(request))




