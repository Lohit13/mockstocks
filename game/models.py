from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model for User
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	institute = models.TextField()
	# TO DO - other game fields
	cash = models.BigIntegerField(default=10000)
	networth = models.BigIntegerField(default=10000)

	def __unicode__(self):
		return self.user.get_full_name()


# Model for a company
class Company(models.Model):
	# Company name
	name = models.CharField(max_length=50)
	# Ticker symbol
	ticker = models.CharField(max_length=10)
	# Field the company is in
	industry = models.CharField(max_length=20)
	# Company turnover
	turnover = models.BigIntegerField(default=0)
	# Quarterly profit
	profit = models.BigIntegerField(default=0)
	# Total number of shares 
	shares = models.IntegerField(default=0)
	# Initial value of shares
	bookvalue = models.IntegerField(default=0)
	# Current price of share
	curprice = models.IntegerField(default=0)
	# Day high
	dayhi = models.IntegerField(default=0)
	# Day low
	daylo = models.IntegerField(default=0)
	# Close price of last day
	close = models.IntegerField(default=0)
	# Net change of share price
	netchange = models.IntegerField(default=0)
	# Year high price
	yearhi = models.IntegerField(default=0)
	# Year low price
	yearlo = models.IntegerField(default=0)
	# price/earning ratio
	peratio = models.IntegerField(default=0)
	# Total number of shares dealt in previous day
	volumes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name


# Offer of share model
class Offer(models.Model):
	# User who offered the shares
	user = models.ForeignKey(UserProfile)
	# Company
	company = models.ForeignKey(Company) 
	# Number of shares offered
	shares = models.IntegerField()
	# Offer price
	price = models.IntegerField()
	# Offered at
	offered_at = models.DateTimeField()


# Transaction model
class Transaction(models.Model):
	# Offer that was bought
	offer = models.ForeignKey(Offer)
	# User that bought the offer
	buyer = models.ForeignKey(UserProfile)
	# Bought at
	bought_at = models.DateTimeField()