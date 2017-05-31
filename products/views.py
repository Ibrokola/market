from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import ProductAddForm, ProductModelForm
from .models import Product
from market.mixins import MultiSlugMixin



class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product


class ProductListView(ListView):
	model = Product
	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		return qs 



def create_view(request):
	#create
	form = ProductModelForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data.get('post'))
		instance = form.save(commit=False)
		instance.save()

	template = "products/form.html"
	context = { 
			"form":form,
			"submit_btn": "Post"
		}
	return render(request, template, context)


def update_view(request, object_id):
	# 1 item
	
	product = get_object_or_404(Product, id=object_id)
	form = ProductModelForm(request.POST or None, instance=product)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
	template = "products/form.html"
	context = { 
			"object":product,
			"form": form,
			"submit_btn": "Update"
		}
	return render(request, template, context)



def detail_slug_view(request, slug=None):
	# 1 item
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by('title').first()
	# print(slug)
	# product = 1
	template = "products/detail_view.html"
	context = { 
			"object":product
		}
	return render(request, template, context)



def detail_view(request, object_id):
	# 1 item
	
	product = get_object_or_404(Product, id=object_id)
	template = "products/detail_view.html"
	context = { 
			"object":product
		}
	return render(request, template, context)




	# if object_id is not None:
	# 	product = get_object_or_404(Product, id=object_id)
	# 	# try:
	# 	# 	product = Product.objects.get(id=object_id)
	# 	# except Product.DoesNotExist:
	# 	# 	product = None
		
	# else:
	# 	raise Http404



	# if request.user.is_authenticated:
	# 	product = Product.objects.all().first()
	# 			
	# else:
	# 	template = "not_found.html"
	# 	context = { }
		


def list_view(request):
	#lis of items

	queryset = Product.objects.all()
	template = "products/list_view.html"
	context = { 
		"queryset":queryset
	}
	return render(request, template, context)
