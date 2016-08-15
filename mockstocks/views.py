from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from game.models import *
from game.views import get_networth
from operator import itemgetter

import requests
import json

from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField


class SignUpForm(forms.ModelForm):

	name = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class' : 'form-control',
																				  'placeholder' : 'Name',
																				  'autocomplete' : 'off',
																				  'name' : 'name'}))

	phone = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class' : 'form-control',
																				  'placeholder' : 'Phone Number',
																				  'autocomplete' : 'off',
																				  'name' : 'phone',
																				  'pattern' : "[1-9][0-9]{9}"}))

	email = forms.EmailField(required = True, widget = forms.EmailInput(attrs = {'class' : 'form-control',
																				 'placeholder' : 'Email id',
																				 'autocomplete' : 'off',
																				 'name' : 'email',
																				 'pattern' : "[^@]+@[^@]+\.[a-zA-Z]{2,6}"}))

	institute = forms.CharField(required = True, widget = forms.TextInput(attrs = {'class' : 'form-control',
																				 	 'placeholder' : '',
																				 	 'autocomplete' : 'off',
																				 	 'name' : 'institute'}))

	password = forms.CharField(required = True, widget = forms.PasswordInput(attrs = {'class' : 'form-control',
																					  'placeholder' : 'Something Secure',
																					  'name' : 'pass'}))

	captcha = NoReCaptchaField()

	class Meta:
		model = User
		fields = ('username', 'password', 'email')


# Home page of app
def index(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/dashboard')
	args = {}
	args.update(csrf(request))
	return render_to_response('index.html', args)


# Rules page
def howto(request):
	return render_to_response('howto.html')


# Logs the user out
def logout(request):
	auth_logout(request)
	args = {}
	args.update(csrf(request))
	return HttpResponseRedirect('/')


# Password check
def check_password(password):
	err = True
	if len(password) < 8:
		err = False
	if not all(x.isalpha() or x.isdigit() or x=='_' for x in password):
		err = False
	return err


# Creates new user
def create_user(details):
	try:
		# Create user
		user = User.objects.create_user(details['phno'],details['email'],details['password'])
		user.first_name = details['name']
		user.save()
		# Create user profile
		u = UserProfile(user=user,institute=details['institute'])
		u.save()
		u.corelate()
		return True
	except:
		return False


# New Registration
def register(request):
	args = {}
	args.update(csrf(request))

	if request.method == 'POST':

		form = SignUpForm(request.POST)

		captach_response = requests.post("https://www.google.com/recaptcha/api/siteverify",
										 data={'secret': "6LcbFg4TAAAAAITqrBWuwH2S9GOk_zO10quel8E1",
											   'response': request.POST["g-recaptcha-response"]})

		verdict = json.loads(captach_response.text)['success']

		state = False

		if verdict == True:

			if form.is_valid():
				state = True

			elif 'captcha' in form.errors.keys():
				form.errors.pop('captcha')
				state = True

		else:
			args['form'] = form
			return render_to_response("register.html", args)

		if state == True:

			if User.objects.filter(username = request.POST["name"]).exists():
				args['form'] = form
				return render_to_response("register.html", args)

			elif User.objects.filter(email = request.POST["email"]).exists():

				form.add_error(None, "Email ID already registered :(")
				args['form'] = form
				return render_to_response("register.html", args)

			else:
				user = User.objects.create_user(username = request.POST["phone"],
												password = request.POST["password"],
												email 	 = request.POST["email"])
				user.first_name = request.POST['name']
				user.save()

				u = UserProfile(user = user, institute = request.POST['institute'])
				u.save()

				return render_to_response("index.html", args)
		else:
			args['form'] = form
			return render_to_response("register.html", args)

	args["form"] = SignUpForm()
	return render_to_response('register.html',args)


# Leaderboard 
def leaderboard(request):
	args = {}
	us = UserProfile.objects.all()
	users = []
	for u in us:
		l = {}
		l['user'] = u
		l['networth'] = get_networth(u)
		users.append(l)
	users = sorted(users, key=itemgetter('networth'))
	args['users'] = users
	return render_to_response('leaderboard.html',args)


# Sign in
def sign_in(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
		    # authenticate the request with the user
		    login(request, user)
		    return HttpResponseRedirect('/dashboard')
		else:
		    # Wrong creds
		    return HttpResponseRedirect('/')