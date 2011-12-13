from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

from pyleads.accounts.forms import UserForm, LoginForm
from pyleads.profiles.models import UserProfile


def register(request, type=''):
	user = request.user
	
	account_type = {'buyer':'Buyer Account', 'publisher':'Publisher Account'}
	
	if request.method == 'POST':
		form = UserForm(request.POST)
		
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			email = form.cleaned_data.get('email')

			newuser = User.objects.create_user(username=username, email=email, password=password)
			newuser.save()
			
			if type == 'publisher':
				g = Group.objects.get(name='publisher')
				newuser.groups.add(g)
			else:
				g = Group.objects.get(name='buyer')
				newuser.groups.add(g)
			
			# Create the profile
			profile = UserProfile(user=newuser, balance=0)
			profile.save()
			
			return HttpResponseRedirect('/'+type+'/')
	else:
		form = UserForm()

	return render_to_response('accounts/register.html', {'form':form, 'account_type':account_type[type]})
	
def do_login(request):
	errors = ""
	
	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			group = form.cleaned_data.get('group')
			
			user = authenticate(username=username, password=password)
			
			if user is not None:
				if user.is_active:
					if user.groups.filter(name=group).count() >  0:
						login(request, user)
						if request.GET.get('next'):
							return HttpResponseRedirect(request.GET['next'])
						else:
							return HttpResponseRedirect("/"+group)	
					else:
						errors = "Your group selection is invalid"
				else:
					errors = "Your account is inactive."
			else:
				errors = "Account information is invalid."
	else:
		form = LoginForm()
	
	return render_to_response('accounts/login.html', {'form':form, 'errors':errors})
	
def logout(request, send='/'):
	from django.contrib.auth import logout
	
	logout(request)
	return HttpResponseRedirect(send)