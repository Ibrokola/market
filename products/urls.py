from django.conf.urls import url, include
from django.contrib import admin

# from .views import detail_view, list_view
from . import views 


urlpatterns = [
	url(r'^detail/$', views.detail_view, name='detail_view'),
	url(r'^list/$', views.detail_view, name='list_view'),
]