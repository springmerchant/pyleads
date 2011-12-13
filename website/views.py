from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext

def main(request):
	return render_to_response('main.html', {}, RequestContext(request))


def contact(request):
	return render_to_response('contact.html', {}, RequestContext(request))

def about(request):
	return render_to_response('about.html', {}, RequestContext(request))