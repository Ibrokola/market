from django.conf.urls import url, include
from django.contrib import admin


from .views import (
					SellerDashboard,
					SellerTransactionListView,
					SellerProductDetailRedirectView
				)
from products.views import (
					ProductCreateView,
					SellerProductListView,
					ProductUpdateView,
				)


urlpatterns = [
    url(r'^$', SellerDashboard.as_view(), name='dashboard'),
    url(r'^transactions/$', SellerTransactionListView.as_view(), name='transactions'),
    url(r'^products/$', SellerProductListView.as_view(), name='product_list'),
    url(r'^products/(?P<pk>\d+)/$', SellerProductDetailRedirectView.as_view()),
    url(r'^products/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='product_edit'),
    url(r'^products/add/$', ProductCreateView.as_view(), name='product_create'),
]