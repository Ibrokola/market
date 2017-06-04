from __future__ import unicode_literals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

from sellers.models import SellerAccount



def download_media_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)



class Product(models.Model):
	seller = models.ForeignKey(SellerAccount)
	# user = models.ForeignKey(settings.AUTH_USER_MODEL)
	# managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_managers', blank=True)
	title = models.CharField(max_length=120, null=True)
	slug = models.SlugField(blank=True, unique=True)
	make = models.CharField(max_length=120, null=True, blank=True, verbose_name='model')
	media = models.ImageField(
						upload_to=download_media_location,
						null=True,
						blank=True,
						storage=FileSystemStorage(location=settings.PROTECTED_ROOT)
					)
	age = models.CharField(max_length=120, null=True, blank=True, help_text='Ignore if not applicable')
	#production date (for perishable goods)
	#expiry date (for perishable goods)
	description = models.TextField()
	price_1 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='Market price')
	price_2_active = models.BooleanField(default=False)
	price_2 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='My price') #100.00


	def __str__(self):
		return self.title

	# def __unicode__(self):
	# 	return u"%s" % (self.media)


	def get_absolute_url(self):
		view_name = "products:detail_slug"
		return reverse(view_name, kwargs={"slug": self.slug}) #args=(self.slug)

	def get_edit_url(self):
		view_name = "sellers:product_edit"
		return reverse(view_name, kwargs={"pk": self.id}) #args=(self.slug)


	def get_download(self):
		view_name = "products:download_slug"
		url = reverse(view_name, kwargs={"slug": self.slug})
		return url

	@property
	def get_price(self):
		if self.price_2 and self.price_2_active:
			return self.price_2
		return self.price_1


	def get_html_price(self):
		price = self.get_price
		if price == self.price_2:
			return "<p>%s</p>" %(self.price_2)
		else:
			return "<p>%s</p>" %(self.price_1)


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug

	qs = Product.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug



def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:	
		instance.slug = create_slug(instance)


pre_save.connect(product_pre_save_reciever, sender=Product, weak=False)



def thumbnail_location(instance, filename):
	return "%s/%s" %(instance.product.slug, filename)

THUMB_CHOICES = (
		("hd", "HD"),
		("sd", "SD"),
		("micro", "Micro"),
	)

class Thumbnail(models.Model):
	product = models.ForeignKey(Product)
	# user = models.ForeignKey(settings.AUTH_USER_MODEL)
	type = models.CharField(max_length=20, choices=THUMB_CHOICES, default="hd")
	height = models.CharField(max_length=120, null=True, blank=True)
	width = models.CharField(max_length=120, null=True, blank=True)
	media = models.ImageField(
						width_field='width',
						height_field='height',
						upload_to=thumbnail_location,
						null=True,
						blank=True,
					)

	def __str__(self):
		return str(self.media.path)

import os
import shutil
from PIL import Image
import random

from django.core.files import File


def create_new_thumb(media_path, owner_slug, instance, max_length, max_width):
	filename = os.path.basename(media_path)
	thumb = Image.open(media_path)
	size = (max_length, max_width)
	thumb.thumbnail(size, Image.ANTIALIAS)
	temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, owner_slug)
	if not os.path.exists(temp_loc):
		os.makedirs(temp_loc)
	temp_file_path = os.path.join(temp_loc, filename)
	if os.path.exists(temp_file_path):
		temp_path = os.path.join(temp_loc, "%s" %(random.random()), filename)
		os.makedirs(temp_path)
		temp_file_path = os.path.join(temp_path, filename)
	temp_image = open(temp_file_path, "wb")
	thumb.save(temp_image)
	thumb_data = open(temp_file_path, "rb")
	thumb_file = File(thumb_data)
	instance.media.save(filename, thumb_file)
	shutil.rmtree(temp_loc, ignore_errors=True)
	return True


def product_post_save_receiver(sender, instance, created, *args, **kwargs):
	if instance.media:
		hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
		sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
		micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

		hd_max = (500, 500)
		sd_max = (350, 350)
		micro_max = (150, 150)

		media_path = instance.media.path
		owner_slug = instance.slug

		if hd_created:
			create_new_thumb(media_path, owner_slug, hd, hd_max[0], hd_max[1])
			# filename = os.path.basename(instance.media.path)
			# thumb = Image.open(instance.media.path)
			# thumb.thumbnail(hd_max, Image.ANTIALIAS)
			# temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, instance.slug)
			# if not os.path.exists(temp_loc):
			# 	os.makedirs(temp_loc)
			# temp_file_path = os.path.join(temp_loc, filename)
			# if os.path.exists(temp_file_path):
			# 	temp_path = os.path.join(temp_loc, "%s" %(random.random()), filename)
			# 	os.makedirs(temp_path)
			# 	temp_file_path = os.path.join(temp_path, filename)
			# temp_image = open(temp_file_path, "wb")
			# thumb.save(temp_image)
			# thumb_data = open(temp_file_path, "rb")
			# thumb_file = File(thumb_data)
			# hd.media.save(filename, thumb_file)


		if sd_created:
			create_new_thumb(media_path, owner_slug, sd, sd_max[0], sd_max[1])

		if micro_created:
			create_new_thumb(media_path, owner_slug, micro, micro_max[0], micro_max[1])




post_save.connect(product_post_save_receiver, sender=Product)





class MyProducts(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	products = models.ManyToManyField(Product, blank=True)


	def __str__(self):
		return "%s" %(self.products.count())

	class Meta:
		verbose_name = 'My products'
		verbose_name_plural = 'My products'


class CuratedProducts(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	section_name = models.CharField(max_length=120)
	products = models.ManyToManyField(Product, blank=True)
	active = models.BooleanField(default=True)


	def __str__(self):
		return self.section_name