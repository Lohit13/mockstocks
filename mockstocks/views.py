from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from game.models import *


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
		return True
	except:
		return False


# New Registration
def register(request):
	args = {}
	args.update(csrf(request))

	if request.method == 'POST':
		err = 0
		args['error'] = ''
		email = request.POST['email']
		password = request.POST['password']
		name = request.POST['name']
		institute = request.POST['institute']
		phno = request.POST['phno']

		# Form validations
		if len(email) < 7:
			err = 1
			args['erremail'] = 'Enter a valid email address'
		if len(name) < 1 or not all(x.isalpha() or x.isspace() for x in name):
			err = 1
			args['errname'] = 'Name should consist of letters and spaces only'
		if not check_password(password):
			err = 1
			args['errpass'] = 'Password should consist of letters, numbers and underscores only. Mininum length is 8 characters'
		if len(institute) < 1 or not all(x.isalpha() or x.isspace() for x in institute):
			err = 1
			args['errinst'] = 'Institute should consist of letters and spaces only'
		if len(phno) != 10 and not isdigit(phno):
			err = 1
			args['errphno'] = 'Enter 10 digit mobile number'

		# In case of no error, create user
		if err == 0:
			if create_user({'name':name,'email':email,'password':password,'institute':institute,'phno':phno}):
				args['success'] = 'Registration successful! You may now login and start playing.'
			else:
				args['data'] = request.POST
				args['failure'] = 'An error occured while creating account. Please check the details and try again'

	return render_to_response('register.html',args)


# Leaderboard 
def leaderboard(request):
	return render_to_response('leaderboard.html')


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