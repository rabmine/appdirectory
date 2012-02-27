from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from app import views as app_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))

urlpatterns += patterns('',
    url(r'^artist/(?P<artist_name>\w+)$', app_views.artist_applications, name="artist_applications"),
    url(r'^ios/iphone', app_views.iphone, name="iphone"),
    url(r'^ios/ipad', app_views.ipad, name="ipad"),
    url(r'^ios/ipod', app_views.ipod, name="ipod"),
    url(r'^ios/', app_views.ios, name="ios"),
    url(r'^mac', app_views.mac, name="mac"),
    url(r'^search', app_views.search, name="search"),
    url(r'^detail/(\d{2,10})$', app_views.detail, name="app_detail"),
    url(r'$', app_views.home, name="home"),
)


