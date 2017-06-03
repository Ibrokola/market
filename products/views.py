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
from .models import Product, MyProducts
from market.mixins import (
					MultiSlugMixin,
					SubmitBtnMixin,
					StaffRequiredMixin,
					LoginRequiredMixin
				)
from analytics.models import TagView
from tags.models import Tag
from .mixins import ProductManagerMixin

from sellers.mixins import SellerAccountMixin



class ProductCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
	model = Product
	template_name = 'products/form.html'
	form_class = ProductModelForm
	# success_url = '/products/add/'
	submit_btn = 'Add product'	


	def form_valid(self, form):
		# user = self.request.user
		# form.instance.user = user
		seller = self.get_account()
		form.instance.seller = seller
		valid_data = super(ProductCreateView, self).form_valid(form) 
		# form.instance.managers.add(user)
		# add all default users
		tags = form.cleaned_data.get('tags')
		if tags:
			tags_list = tags.split(',')
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(form.instance)
		return valid_data 



class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product


	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		tags = obj.tag_set.all()
		if self.request.user.is_authenticated():
			for tag in tags:
				new_view = TagView.objects.add_count(self.request.user, tag)
		return context



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

	def get_initial(self):
		initial = super(ProductUpdateView, self).get_initial()
		tags = self.get_object().tag_set.all()
		initial["tags"] = ", ".join([x.title for x in tags])
		return initial

	def form_valid(self, form):
		valid_data = super(ProductUpdateView, self).form_valid(form) 
		tags = form.cleaned_data.get('tags')
		obj = self.get_object()
		obj.tag_set.clear()
		if tags:
			tags_list = tags.split(',')
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(self.get_object())
		return valid_data 




class SellerProductListView(SellerAccountMixin, ListView):
	model = Product
	template_name = "sellers/product_list_view.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(SellerProductListView, self).get_queryset(*args, **kwargs)
		qs = qs.filter(seller=self.get_account())
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
						Q(title__icontains=query) |
						Q(description__icontains=query) |
						Q(price_1__icontains=query) |
						Q(price_2__icontains=query)
					).order_by('-pk')
		return qs 


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


class UserLibraryListView(LoginRequiredMixin, ListView):
	model = Product
	template_name = "products/library_list.html"

	def get_queryset(self, *args, **kwargs):
		obj = MyProducts.objects.get_or_create(user=self.request.user)[0]
		qs = obj.products.all()
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
