from django.contrib import admin
from game.models import *

# Register your models here.

Models = [UserProfile, Company, Offer, Transaction, Corelate]

admin.site.register(Models)
