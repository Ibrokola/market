from __future__ import unicode_literals
import os

from mimetypes import guess_type

from django.conf import settings
from django.utils.encoding import force_bytes
from wsgiref.util import FileWrapper
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ProductAddForm, ProductModelForm
from .models import Product
from market.mixins import (
					MultiSlugMixin,
					SubmitBtnMixin,
					StaffRequiredMixin,
					LoginRequiredMixin
				)

from .mixins import ProductManagerMixin



class ProductCreateView(LoginRequiredMixin, SubmitBtnMixin, CreateView):
	model = Product
	template_name = 'products/form.html'
	form_class = ProductModelForm
	# success_url = '/products/add/'
	submit_btn = 'Add product'	


	def form_valid(self, form):
		user = self.request.user
		form.instance.user = user
		valid_data = super(ProductCreateView, self).form_valid(form) 
		form.instance.managers.add(user)
		# add all default users
		return valid_data 

	# def get_success_url(self):
	# 	return reverse('products: list')


class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product

class ProductDownloadView(MultiSlugMixin, DetailView):
	model = Product
	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj in request.user.myproducts.products.all():
			filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
			guessed_type = guess_type(filepath)[0] 
			wrapper = FileWrapper(open(filepath, 'rb'))
			mimetype = 'application/force-download'

			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, content_type=mimetype)


			if not request.GET.get("preview"):
				response["Content-Disposition"] = "attachement; filename = %s" %(obj.media.name)

			response["X-SendFile"] = str(obj.media.name)
			return response
		else:
			raise Http404
		# print(dir(open))



class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = 'products/form.html'
	form_class = ProductModelForm
	# success_url = '/products/'
	submit_btn = 'Update product'


class ProductListView(ListView):
	model = Product
	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
						Q(title__icontains=query) |
						Q(description__icontains=query) |
						Q(price_1__icontains=query) |
						Q(price_2__icontains=query)
					).order_by('-pk')
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
