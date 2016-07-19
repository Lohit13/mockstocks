from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model for User
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	institute = models.TextField()
	# TO DO - other game fields

	def __unicode__(self):
		return self.user.get_full_name()