from django import forms

from django.utils.text import slugify
from .models import Product



POST_CHOICES = (
		('post', "Post"),
		('draft', "Draft"),
		('update', "Update"),
	)

class ProductAddForm(forms.Form):
	title = forms.CharField(label='Product name' ,widget=forms.TextInput(attrs={
			'class': 'custom-class',
			'placeholder': 'Title',
		}))
	make = forms.CharField()
	age = forms.CharField()
	#production date (for perishable goods)
	#expiry date (for perishable goods)
	description = forms.CharField(widget=forms.Textarea(
			attrs={
				'class': 'my-custom-class',
				'placeholder': 'Description',
				'some-attr': 'this',
			}
		))
	price_1 = forms.DecimalField(label='Market price') #
	price_2 = forms.DecimalField(label='My price') #
	post = forms.ChoiceField(widget=forms.RadioSelect, choices=POST_CHOICES)

	def clean_price_2 (self):
		price_2 = self.cleaned_data.get('price_2')
		if price_2 <= 1.00:
			raise forms.ValidationError('Price must be greater than $1.00')
		elif price_2 >= 99.99:
			raise forms.ValidationError('Price must be less than $100')
		else:
			pass
		return price_2


	def clean_title (self):
		title = self.cleaned_data.get('title')
		if len(title) >= 5:
			return title
		else:
			raise forms.ValidationError('Product name must be more than five(5) charcters long')



class ProductModelForm(forms.ModelForm):
	tags = forms.CharField(label='Related tags', required=False)
	# post = forms.ChoiceField(widget=forms.RadioSelect, choices=POST_CHOICES)
	class Meta:
		model = Product
		fields = [
			'title',
			'make',
			'age',
			'description',
			'price_1',
			'price_2',
		]


	def clean(self, *args, **kwargs):
		cleaned_data = super(ProductModelForm, self).clean(*args, **kwargs)
		# title= cleaned_data.get('title')
		# slug = slugify(title)
		# qs = Product.objects.filter(slug=slug).exists()
		# if qs:
		# 	raise forms.ValidationError('Title taken, please provide a diffrent title')
		# return cleaned_data


	# def clean_price_2 (self):
	# 	price_2 = self.cleaned_data.get('price_2')
	# 	if price_2 <= 1.00:
	# 		raise forms.ValidationError('Price must be greater than $1.00')
	# 	elif price_2 >= 99.99:
	# 		raise forms.ValidationError('Price must be less than $100')
	# 	else:
	# 		pass
	# 	return price_2


	# def clean_title (self):
	# 	title = self.cleaned_data.get('title')
	# 	if len(title) >= 5:
	# 		return title
	# 	else:
	# 		raise forms.ValidationError('Product name must be more than five(5) charcters long')
