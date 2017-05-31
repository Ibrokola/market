from django.conf.urls import url, include
from django.contrib import admin

from products import views
from products.views import (
					ProductCreateView,
					ProductListView,
					ProductDetailView,
					ProductUpdateView
				) 

urlpatterns = [
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^notifications/', include('pinax.notifications.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^review/', include('review.urls')),
    url(r'^', include('django_private_chat.urls')),
    # url(r'^products/', include('products.urls')),
    url(r'^create/$', views.create_view, name='create_view'),
    url(r'^detail/(?P<object_id>\d+)/edit/$', views.update_view, name='update_view'),
    url(r'^detail/(?P<object_id>\d+)/$', views.detail_view, name='detail_view'),
    url(r'^detail/(?P<slug>[\w-]+)/$', views.detail_slug_view, name='detail_slug_view'),
    url(r'^list/$', views.list_view, name='list_view'),
    url(r'^products/$', ProductListView.as_view(), name='product_list_view'),
    url(r'^products/add/$', ProductCreateView.as_view(), name='product_create_view'),
    url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail_view'),
    url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail_slug_view'),
    url(r'^products/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='product_update_view'),
    url(r'^products/(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='product_update_slug_view'),
]
# 