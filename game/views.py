from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from game.models import *

# Create your views here.

def get_rank(user):
	users = UserProfile.objects.order_by('networth')
	print users
	i = 1
	for u in users:
		if u == user:
			break
		i += 1
	return i


@login_required(login_url='/',redirect_field_name=None)
def dashboard(request):
	user = UserProfile.objects.get(user=request.user)
	args = {}
	args['user'] = user
	args['rank'] = get_rank(user)
	co = Corelate.objects.filter(user=user)
	shares = []
	for c in co:
		if c.shares > 0:
			shares.append(c)
	args['shares'] = shares
	return render_to_response('dashboard.html',args)


# Transaction history of company for user
def history(request):
	return render_to_response('history.html')


# All companies
def companies(request):
	return render_to_response('companies.html')


# Sell shares
def sell(request):
	user = UserProfile.objects.get(user=request.user)
	offers = Offer.objects.filter(user=user,active=True)
	args = {}
	args['offers'] = offers
	return render_to_response('sell.html',args)


# Buy shares
def buy(request):
	return render_to_response('buy.html')