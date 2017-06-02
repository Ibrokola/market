import random
from django.views import View
from django.shortcuts import render

from products.models import Product


class DashboardView(View):
	def get(self, request, *args, **kwargs):
		views = None
		products = None
		top_tags = None
		try:
			tag_views=request.user.tagview_set.all().order_by('-count')[:5]
		except:
			pass

		owned = None
		try:
			owned = request.user.myproducts.products.all()
		except:
			pass

		if tag_views:
			top_tags = [x.tag for x in tag_views]
			products = Product.objects.filter(tag__in=top_tags)
			if owned:
				products = products.exclude(pk__in=owned)

			if products.count() < 10:
				products = Product.objects.all().order_by('?')
				if owned:
					products = products.exclude(pk__in=owned)
				products = products[:10]
			else:
				products = products.distinct()
				products = sorted(products, key= lambda x: random.random())
		template = "dashboard/view.html"
		context = {
			"products":products,
			"top_tags":top_tags,
		}
		return render(request, template, context)