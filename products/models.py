from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify





class Product(models.Model):
	title = models.CharField(max_length=120, null=True)
	slug = models.SlugField(blank=True) #unique=True
	make = models.CharField(max_length=120, null=True, blank=True, verbose_name='model')
	age = models.CharField(max_length=120, null=True, blank=True, help_text='Ignore if not applicable')
	#production date (for perishable goods)
	#expiry date (for perishable goods)
	description = models.TextField()
	price_1 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='Market price')
	price_2 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='My price') #100.00


	def __str__(self):
		return self.title



def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:	
		instance.slug = slugify(instance.title)


pre_save.connect(product_pre_save_reciever, sender=Product, weak=False)



# def product_post_save_reciever(sender, instance, *args, **kwargs):
# 	if instance.slug != slugify(instance.title):	
# 		instance.slug = slugify(instance.title)
# 		instance.save()

# post_save.connect(product_post_save_reciever, sender=Product, weak=False)