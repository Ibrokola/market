from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^notifications/', include('pinax.notifications.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^review/', include('review.urls')),
    url(r'^', include('django_private_chat.urls')),
]
# 