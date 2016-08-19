from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model for User
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	institute = models.TextField()
	# TO DO - other game fields
	cash = models.BigIntegerField(default=100000)

	def __unicode__(self):
		return self.user.get_full_name()

	def corelate(self):
		companies = Company.objects.all()
		for company in companies:
			c = Corelate(user=self,company=company)
			c.save()


# Model for a company
class Company(models.Model):
	# Company name
	name = models.CharField(max_length=50)
	# Ticker symbol
	ticker = models.CharField(max_length=10)
	# Field the company is in
	industry = models.CharField(max_length=20)
	# Quarterly profit
	profit = models.BigIntegerField(default=0)
	# Total number of shares 
	shares = models.IntegerField(default=0)
	# Shares for initial buyin
	initshares = models.IntegerField(default=0)
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
	# Volume of next day
	nextvol = models.BigIntegerField(default=0)
	# Just to see close
	nextclose = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name


# Offer of share model
class Offer(models.Model):
	# User who offered the shares
	user = models.ForeignKey(UserProfile, blank=True, null=True)
	# Company
	company = models.ForeignKey(Company)
	# Number of shares offered
	shares = models.IntegerField()
	# Offer price
	price = models.IntegerField()
	# Offered at
	offered_at = models.DateTimeField()
	# If not bought, then active is true
	active = models.BooleanField(default=True)


# Transaction model
class Transaction(models.Model):
	# Offer that was bought
	offer = models.ForeignKey(Offer)
	# User that bought the offer
	buyer = models.ForeignKey(UserProfile)
	# Bought at
	bought_at = models.DateTimeField()

# Model to corelate user and company
class Corelate(models.Model):
	user = models.ForeignKey(UserProfile)
	company = models.ForeignKey(Company)
	shares = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.user.user.first_name)


# News
class News(models.Model):
	news = models.TextField()
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.news