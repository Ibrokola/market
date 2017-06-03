from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView


from market.mixins import LoginRequiredMixin

from .forms import NewSellerForm
from .models import SellerAccount
from .mixins import SellerAccountMixin

from billing.models import Transaction
from products.models import Product



class SellerProductDetailRedirectView(RedirectView):

    permanent = True
    # query_string = True
    # pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()


class SellerTransactionListView(SellerAccountMixin, ListView):
	model = Transaction
	template_name = "sellers/transaction_list_view.html"

	def get_queryset(self):
		return self.get_transactions()


class SellerDashboard(SellerAccountMixin, FormMixin, View):
	form_class = NewSellerForm
	success_url = '/seller/'

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
		    return self.form_valid(form)
		else:
		    return self.form_invalid(form)


	def get(self, request, *args, **kwargs):
		apply_form = NewSellerForm()
		# account = SellerAccount.objects.filter(user=self.request.user)
		account = self.get_account()
		exists = account
		active = None
		template = 'sellers/dashboard.html'
		context = {}
		if exists:
			# account = account.first()
			active = account.active
		if not exists and not active:
			context["title"] = "Apply for Account"
			context["apply_form"] = apply_form
		elif exists and not active:
			context["title"] = "Account Pending"
		elif exists and active:
			context["title"] = "Seller Dashboard"
			# products = Product.objects.filter(seller=account)
			context["products"] = self.get_products()
			transactions = self.get_transactions()
			transactions_today = self.get_transactions_today()
			context["transactions_today"] = transactions_today
			context["today_sales"] = self.get_today_sales()
			context["total_sales"] = self.get_total_sales()
			context["transactions"] = transactions[:5] #.exclude(pk__in=transactions_today)
		else:
			pass

		return render(request, template, context)


	def form_valid(self, form):
		valid_data = super(SellerDashboard, self).form_valid(form) 
		obj = SellerAccount.objects.create(user=self.request.user)
		return valid_data 


