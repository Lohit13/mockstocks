from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from game.models import *

# Create your views here.

@login_required(login_url='/',redirect_field_name=None)
def dashboard(request):
	user = UserProfile.objects.get(user=request.user)
	args = {}
	args['user'] = user
	return render_to_response('dashboard.html',args)


# Transaction history of company for user
def history(request):
	return render_to_response('history.html')


# All companies
def companies(request):
	return render_to_response('companies.html')


# Sell shares
def sell(request):
	return render_to_response('sell.html')


# Buy shares
def buy(request):
	return render_to_response('buy.html')