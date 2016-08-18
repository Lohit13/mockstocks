from celery import task
import datetime
from game.models import *

# Task for transaction
@task(name='buyOffer')
def buyOffer(user, offer, netchange):
	# Company whose shares are being dealt
	company = offer.company
	# Seller (buyer is user passed)
	seller = offer.user
	# Total value of offer
	total = offer.shares * offer.price

	# Corelate objects of buyer and seller
	cobuyer = Corelate.objects.get(company=company,user=user)
	coseller = Corelate.objects.get(company=company,user=seller)

	# Make the offer inactive
	offer.active = False
	offer.save()

	# Add and subtract accordingly
	cobuyer.shares = cobuyer.shares + offer.shares
	coseller.shares = coseller.shares - offer.shares
	seller.cash = seller.cash + total
	user.cash = user.cash - total

	# Make a new transaction
	trans = Transaction(offer=offer,buyer=user,bought_at=datetime.datetime.now())
	trans.save()

	# Commit the changes
	user.save()
	seller.save()
	coseller.save()
	cobuyer.save()

	# Make changes to Company
	company.netchange = netchange

	company.curprice = offer.price
	if(offer.price > company.dayhi):
		company.dayhi = offer.price
	if(offer.price < company.daylo):
		company.daylo = offer.price
	if(offer.price > company.yearhi):
		company.yearhi = offer.price
	if(offer.price < company.yearlo):
		company.yearlo = offer.price
	company.nextvol = company.nextvol + offer.shares

	company.nextclose = offer.price

	company.save()

	return

# Task for initbuy
@task(name='initBuy')
def initBuy(user, com, shares):
	# Corelate object of buyer
	cobuyer = Corelate.objects.get(company=com,user=user)

	total = int(shares)*com.curprice

	# Create offer for company
	offer = Offer(user=None, company=com, shares=int(shares), price=com.curprice, offered_at=datetime.datetime.now(), active=False)
	offer.save()

	# Create the transaction
	trans = Transaction(offer=offer, buyer=user, bought_at=datetime.datetime.now())

	cobuyer.shares = cobuyer.shares + offer.shares
	com.initshares = com.initshares - offer.shares
	com.nextvol = com.nextvol + offer.shares
	user.cash = user.cash - total

	trans.save()
	com.save()
	user.save()
	cobuyer.save()

	return