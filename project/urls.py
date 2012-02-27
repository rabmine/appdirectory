from django.conf import settings
from django.conf.urls.defaults import patterns, url

from app import views as app_views
from django.views.generic.base import RedirectView
from app.views import DeviceAppListView, ArtistAppListView, SearchAppListView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))

urlpatterns += patterns('',
    url(r'^$', RedirectView.as_view(url='device/ios/'), name="home"),
    
    url(r'^device/(?P<device>\w+)/$', DeviceAppListView.as_view(), name="device"),
    url(r'^artist/(?P<artist_name>\w+)/$', ArtistAppListView.as_view(), name="artist_applications"),
    url(r'^search', SearchAppListView.as_view(), name="search"),
    
    url(r'^detail/(\d{2,10})$', app_views.detail, name="app_detail"),
)


