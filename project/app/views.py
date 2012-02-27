from django.views.generic.list import ListView
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView

from models import Application, DeviceType

class HomeView(TemplateView):
    template_name = "index.html"

class AppDetailView(TemplateView):
    template_name = "app_detail.html"
    
class BaseAppListView(ListView):
    """ Base view for application lists on the main page. """
    
    template_name = "index.html"
    paginate_by = settings.RESULTS_PAGE_LENGTH
    
    
class DeviceAppListView(BaseAppListView):
    def get_context_data(self, **kwargs):
        
        context =  ListView.get_context_data(self, **kwargs)
        context['device'] = self.kwargs['device']
        return context
    
    def get_queryset(self):
        
        device = self.kwargs['device']
        
        if device == "ios":
            device_types = DeviceType.objects.exclude(name__istartswith="mac")
  
        else:
            device_types = DeviceType.objects.filter(name__istartswith=device)
        
        return Application.objects.filter(applicationdevicetype__device_type__in=device_types)

class SearchAppListView(BaseAppListView):
    def get_queryset(self):
        keywords = self.request.GET.get("q", "")
        
        return Application.objects.filter(Q(title__search=keywords) | 
                                          Q(description__search=keywords)).distinct()

class ArtistAppListView(BaseAppListView):
    
    def get_queryset(self):
        artist_name = self.kwargs['artist_name']
        return Application.objects.filter(artist_name=artist_name)

def detail(request, id):
    application = get_object_or_404(Application, application_id=id)
    view_data = dict(app=application)
    return render_to_response("app_detail.html", view_data)
