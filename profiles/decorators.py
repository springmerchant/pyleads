from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlquote

def publisher_required(func):
	def _wrapper(*args, **kwargs):
		if args[0].user.username == "":	
			return HttpResponseRedirect('/login/')
			
		if args[0].user.groups.filter(name='publisher').count() >  0:
			return func(*args, **kwargs)
		else:
			return HttpResponseRedirect('/login/')

	return _wrapper

def buyer_required(func):
	def _wrapper(*args, **kwargs):
		if args[0].user.username == "":	
			return HttpResponseRedirect('/login/')
			
		if args[0].user.groups.filter(name='buyer').count() >  0:
			return func(*args, **kwargs)
		else:
			return HttpResponseRedirect('/login/')

	return _wrapper