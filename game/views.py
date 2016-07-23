from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from game.models import *
from operator import itemgetter
import datetime
import json

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
	for u in users:
		if u['user'] == user:
			break
		i += 1
	return i


@login_required(login_url='/',redirect_field_name=None)
def dashboard(request):
	user = UserProfile.objects.get(user=request.user)
	args = {}
	args['user'] = user
	args["allcompanies"] = Company.objects.all()
	args['rank'] = get_rank(user)
	co = Corelate.objects.filter(user=user,shares__gt=0)
	args['shares'] = co
	args['networth'] = get_networth(user)
	return render_to_response('dashboard.html',args)


# Transaction history of company for user
@login_required(login_url='/',redirect_field_name=None)
def history(request):
	return render_to_response('history.html')


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
		print args['max']
		jp = json.dumps(args)
		#return JsonResponse(jp,safe=False)
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
		company = Company.objetcs.get(id=cid)
		offer = Offer(user=user,company=company,shares=shares,price=price,offered_at=datetime.datetime.now())
		offer.save()
		return HttpResponseRedirect('/sell')

	return render_to_response('sell.html',args)


# Buy shares
@login_required(login_url='/',redirect_field_name=None)
def buy(request):
	args = {}
	args.update(csrf(request))
	args['companies'] = Company.objects.all()
	if request.method == 'POST':
		cid = request.POST['company']
		company = Company.objects.get(id=cid)
		offers = Offer.objects.filter(company=company,active=True)
		args['user'] = UserProfile.objects.get(user=request.user)
		args['offers'] = offers
		args['post'] = 1
	return render_to_response('buy.html',args)


# Accept an offer
@login_required(login_url='/',redirect_field_name=None)
def buyoffer(request,offer_id):
	user = UserProfile.objects.get(user=request.user)
	offer = Offer.objects.get(id=offer_id)
	company = offer.company
	seller = offer.user
	total = offer.shares*offer.price

	if total > user.cash:
		return HttpResponseRedirect('/buy')

	cobuyer = Corelate.objects.get(company=company,user=user)
	coseller = Corelate.objects.get(company=company,user=seller)

	offer.active = False
	cobuyer.shares = cobuyer.shares+offer.shares
	coseller.shares = coseller.shares-offer.shares
	seller.cash = seller.cash+total
	user.cash = user.cash-total
	tran = Transaction(offer=offer,buyer=user,bought_at=datetime.datetime.now())

	tran.save()
	user.save()
	seller.save()
	coseller.save()
	cobuyer.save()
	offer.save()
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




