from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from .views import (
					ProductCreateView,
					ProductListView,
					ProductDetailView,
					ProductUpdateView,
                    ProductDownloadView,
                    VendorListView
				)


urlpatterns = [

    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^vendor/$', RedirectView.as_view(pattern_name='products:list'), name='vendor_list'),
    url(r'^vendor/(?P<vendor_name>[\w.@+-]+)/$', VendorListView.as_view(), name='vendor_detail'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),
    url(r'^(?P<pk>\d+)/download/$', ProductDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', ProductDownloadView.as_view(), name='download_slug'),
    url(r'^(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='update_slug'),
]