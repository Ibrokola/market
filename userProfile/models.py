from django.conf import settings
from django.db import models


# Create your models here.


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='user name')
	title = models.CharField(max_length=120, verbose_name='Full Name')
	address = models.CharField(max_length=240, null=True, blank=True)
	address_2 = models.CharField(max_length=240, null=True, blank=True)
	member_since =  models.DateField(auto_now_add=True, verbose_name='signup date')
	Biography = models.TextField()

	# member_since 

	def __str__(self):
		return self.title

		# class Meta: