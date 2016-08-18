from django.contrib import admin
from game.models import *

# Register your models here.

Models = [UserProfile, Company, Offer, Transaction, Corelate, News]

admin.site.register(Models)
