from django.db import models







class Product(models.Model):
	title = models.CharField(max_length=120, null=True)
	make = models.CharField(max_length=120, null=True, blank=True, verbose_name='model')
	age = models.CharField(max_length=120, null=True, blank=True, help_text='Ignore if not applicable')
	#production date (for perishable goods)
	#expiry date (for perishable goods)
	description = models.TextField()
	price_1 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='market_price')
	price_2 = models.DecimalField(max_digits=100, decimal_places=2, default=10.99, verbose_name='my_price') #100.00


	def __str__(self):
		return self.title

