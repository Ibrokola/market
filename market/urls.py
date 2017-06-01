from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^notifications/', include('pinax.notifications.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^review/', include('review.urls')),
    url(r'^', include('django_private_chat.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^tags/', include('tags.urls', namespace='tags')),    
]
# 

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)