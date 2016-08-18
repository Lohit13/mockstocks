from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from game.models import *
from operator import itemgetter
import datetime
import json
from itertools import chain
from game.tasks import *

# Returns user's networth
def get_networth(user):
	cos = Corelate.objects.filter(user=user)
	sharevalue = 0
	for co in cos:
		covalue = co.shares*co.company.curprice
		sharevalue = sharevalue + covalue
	networth = user.cash + sharevalue
	return networth


# Returns user's rank
def get_rank(user):
	us = UserProfile.objects.all()
	users = []
	for u in us:
		l = {}
		l['user'] = u
		l['networth'] = get_networth(u)
		users.append(l)
	users = sorted(users, key=itemgetter('networth'))
	i = 1
	for u in users[::-1]:
		if u['user'] == user:
			break
		i += 1
	return i


@csrf_exempt
@login_required(login_url='/',redirect_field_name=None)
def get_curr_prices(request):
	companies = Company.objects.all()
	data = {}
	i = 1
	for company in companies:
		data[i] = [company.ticker,company.curprice,company.netchange]
		i = i + 1
	return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


@login_required(login_url='/',redirect_field_name=None)
def dashboard(request):
	user = UserProfile.objects.get(user=request.user)
	args = {}
	args['user'] = user
	args["allcompanies"] = Company.objects.all()
	try:
		args['news'] = News.objects.order_by('id')[0]
	except:
		pass
	try:
		args['news'] = News.objects.all().reverse()[0]
	except:
		pass
	args['rank'] = get_rank(user)
	co = Corelate.objects.filter(user=user,shares__gt=0)
	args['shares'] = co
	args['networth'] = get_networth(user)
	return render_to_response('dashboard.html',args)


# All companies
@login_required(login_url='/',redirect_field_name=None)
def companies(request):
	args = {}
	args['companies'] = Company.objects.all()
	return render_to_response('companies.html',args)


# View for sell ajax
@csrf_exempt
@login_required(login_url='/',redirect_field_name=None)
def max_shares(request):
	if request.method == 'POST':
		selected = request.POST['selected']
		user = UserProfile.objects.get(user=request.user)
		company = Company.objects.get(id=selected)
		c = Corelate.objects.get(user=user,company=company)
		args = {}
		args['max'] = c.shares
		jp = json.dumps(args)
		return HttpResponse(
            json.dumps(args),
            content_type="application/json"
        )
	else:
		return None


# View for sell ajax
@csrf_exempt
@login_required(login_url='/',redirect_field_name=None)
def get_curr_price(request):
	if request.method == 'POST':
		selected = request.POST['selected']
		company = Company.objects.get(id=selected)
		args = {}
		args['curprice'] = company.curprice
		jp = json.dumps(args)
		return HttpResponse(
            json.dumps(args),
            content_type="application/json"
        )
	else:
		return None


# Sell shares
@login_required(login_url='/',redirect_field_name=None)
def sell(request):
	args = {}
	user = UserProfile.objects.get(user=request.user)
	offers = Offer.objects.filter(user=user,active=True)
	shares = Corelate.objects.filter(user=user,shares__gt=0)
	args['offers'] = offers
	args['shares'] = shares
	args.update(csrf(request))
	if request.method == 'POST':
		cid = request.POST['company']
		shares = request.POST['shares']
		price = request.POST['price']
		company = Company.objects.get(id=cid)
		offer = Offer(user=user,company=company,shares=shares,price=price,offered_at=datetime.datetime.now())
		offer.save()
		return HttpResponseRedirect('/sell')

	return render_to_response('sell.html',args)


# Buy shares
@login_required(login_url='/',redirect_field_name=None)
def buy(request):
	args = {}
	user = UserProfile.objects.get(user=request.user)
	args.update(csrf(request))
	args['companies'] = Company.objects.all()
	args['initcoms'] = Company.objects.filter(initshares__gt=0)
	args['user'] = user
	if request.method == 'POST':
		cid = request.POST['company']
		company = Company.objects.get(id=cid)
		offers = Offer.objects.filter(company=company,active=True).exclude(user=user)
		args['user'] = UserProfile.objects.get(user=request.user)
		args['offers'] = offers
		args['post'] = 1
	return render_to_response('buy.html',args)


@login_required(login_url='/',redirect_field_name=None)
def buyoffer(request,offer_id):
	user = UserProfile.objects.get(user=request.user)
	try:
		offer = Offer.objects.get(id=offer_id)
	except:
		return HttpResponseRedirect('/buy/')

	total = offer.shares*offer.price

	if total > user.cash:
		return HttpResponseRedirect('/buy')

	netchange = offer.price - offer.company.curprice

	buyOffer.delay(user,offer,netchange)

	return HttpResponseRedirect('/dashboard')


# Remove an offer if it's still active
@login_required(login_url='/',redirect_field_name=None)
def remove_offer(request,offer_id):
	user = UserProfile.objects.get(user=request.user)
	offer = Offer.objects.get(id=offer_id)

	if not offer.user == user or offer.active == False:
		return HttpResponseRedirect('/sell')

	offer.delete()

	return HttpResponseRedirect('/sell')


# Transaction history
@login_required(login_url='/',redirect_field_name=None)
def history(request,company_id):
	user = UserProfile.objects.get(user=request.user)
	com = Company.objects.get(id=company_id)
	one = Transaction.objects.filter(offer__company=com).filter(buyer=user)
	two = Transaction.objects.filter(offer__company=com).filter(offer__user=user)
	result = list(chain(one,two))
	result.sort(key=lambda x: x.bought_at, reverse=False)
	args = {}
	args['trans'] = result
	args['com'] = com
	return render_to_response('history.html',args)


# Get company info ajax
@csrf_exempt
@login_required(login_url='/',redirect_field_name=None)
def getinfo(request):
	companies = Company.objects.all()
	data = {}
	for com in companies:
		data[com.id] = [com.initshares, com.curprice]
	return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


# Initshare buy
@login_required(login_url='/',redirect_field_name=None)
def initbuy(request):
	if request.method=='POST':
		user = UserProfile.objects.get(user=request.user)
		com = Company.objects.get(id=request.POST['comid'])
		shares = request.POST['shares']
		total = int(shares)*com.curprice

		if total > user.cash:
			return HttpResponseRedirect('/buy')

		initBuy.delay(user,com,shares)
		
	return HttpResponseRedirect('/')