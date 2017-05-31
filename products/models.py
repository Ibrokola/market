from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify





class Product(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_managers', blank=True)
	title = models.CharField(max_length=120, null=True)
	slug = models.SlugField(blank=True, unique=True)
	make = models.CharField(max_length=120, null=True, blank=True, verbose_name='model')
	age = models.CharField(max_length=120, null=True, blank=True, help_text='Ignore if not applicable')
	#production date (for perishable goods)
	#expiry date (for perishable goods)
	description = models.TextField()
	price_1 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='Market price')
	price_2 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='My price') #100.00


	def __str__(self):
		return self.title


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



# def product_post_save_reciever(sender, instance, *args, **kwargs):
# 	if instance.slug != slugify(instance.title):	
# 		instance.slug = slugify(instance.title)
# 		instance.save()

# post_save.connect(product_post_save_reciever, sender=Product, weak=False)