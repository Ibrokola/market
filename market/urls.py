from jet.dashboard.dashboard_modules import google_analytics_views
from django.conf.urls import url, include
from django.contrib import admin
# from baton.autodiscover import admin
from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import DashboardView
from checkout.views import CheckoutTestView, CheckoutAjaxView
from products.views import UserLibraryListView
# from jet.dashboard.dashboard_modules import google_analytics_views

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^test/$', CheckoutTestView.as_view(), name='test'),
    url(r'^checkout/$', CheckoutAjaxView.as_view(), name='checkout'),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),
    # url(r'^baton/', include('baton.urls')),
    url(r'^notifications/', include('pinax.notifications.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^review/', include('review.urls')),
    url(r'^', include('django_private_chat.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^tags/', include('tags.urls', namespace='tags')),
    url(r'^seller/', include('sellers.urls', namespace='sellers')),
    url(r'^library/', UserLibraryListView.as_view(), name='library'),    
]
# 

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)