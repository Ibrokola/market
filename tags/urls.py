from django.conf.urls import url, include
from django.contrib import admin


from .views import (
					TagListView,
					TagDetailView,
				)


urlpatterns = [
    url(r'^$', TagListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', TagDetailView.as_view(), name='detail'),
    

]