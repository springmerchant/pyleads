import time
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.contrib.auth.models import User

from pyleads.profiles.models import UserProfile
from pyleads.remote.models import LeadView
from pyleads.logs.models import TrackerLog
from pyleads.campaign.models import Campaign, Tracker, FormCss

def index(request):
    try:
        tracker_log = TrackerLog.objects.get(date=datetime.today(), tracker__name=request.GET.get('tracker'))
    except TrackerLog.DoesNotExist:
        # Check to see if the tracker is valid
        try:
            tracker = Tracker.objects.get(name=request.GET.get('tracker'))
        except Tracker.DoesNotExist:
            return HttpResponse("Tracker is invalid.")

        if tracker is not None:
            tracker_log = TrackerLog(date=datetime.today(), tracker=tracker, sold_total=0)

    campaign = tracker_log.tracker.campaign
    campaign.impressions += 1
    campaign.save()

    tracker_log.impressions += 1
    tracker_log.save()

    now = time.localtime(time.time())

    lv = LeadView(trackerlog=tracker_log, time=time.strftime("%Y-%m-%d %H:%M:%S", now), url=request.GET.get('url'))
    lv.save()

    return HttpResponse()

def addclick(request):
    try:
        tracker_log = TrackerLog.objects.get(date=datetime.today(), tracker__name=request.GET.get('tracker'))
    except TrackerLog.DoesNotExist:
        return HttpResponse("Invalid tracker.")

    campaign = tracker_log.tracker.campaign

    campaign.clicks = campaign.clicks + 1
    campaign.save()

    tracker_log.clicks = tracker_log.clicks+1
    tracker_log.save()

    return HttpResponse()

def formcss(request):
    try:
        tracker_log = TrackerLog.objects.get(date=datetime.today(), tracker__name=request.GET.get('tracker'))
    except TrackerLog.DoesNotExist:
        return HttpResponse("Invalid tracker.")

    campaign = tracker_log.tracker.campaign

    try:
        css = tracker_log.tracker.design
    except Exception:
        return HttpResponse("Form Css does not exist.")

    if css is not None:
        valid_css = {"border-color": css.border_color, 
                     "border-width": css.border_width, 
                     "border-style": css.border_style,
                     "background-color": css.bg_color,
                     "color": css.font_color}

        input = {"background-color" : css.input_bg_color,
                 "border-width" : "1px", 
                 "color":css.input_color}

        css = {"form": valid_css, "input" : input}

    return HttpResponse(request.GET['callback']+'('+simplejson.dumps(css)+');')



def javascript(request, type, tracker):
    return render_to_response('javascript.html', {'type':type, 'tracker':tracker})


