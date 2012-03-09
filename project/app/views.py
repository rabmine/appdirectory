from django.views.generic.list import ListView
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404

from models import Application
from app.models import Artist
from django.views.generic.detail import DetailView

class BaseAppListView(ListView):
    """ Base view for application lists on the main page. """
    
    template_name = "index.html"
    paginate_by = settings.RESULTS_PAGE_LENGTH
    context_object_name = 'applications'
    
    def get_queryset(self):
        return Application.objects.all()
    
    
class DeviceAppListView(BaseAppListView):
    
    DEVICE_NAMES = {'ios' : 'iOS', 
                    'mac' : 'Mac',
                    'all' : 'All',
                    'ipod' : 'iPod',
                    'ipad' : 'iPad',
                    'iphone' : 'iPhone'}
    
    def get_context_data(self, **kwargs):
        
        context =  super(DeviceAppListView, self).get_context_data(**kwargs)
        context['device'] = self.kwargs['device']
        
        device_name = self.DEVICE_NAMES.get(self.kwargs['device'], 
                                            self.kwargs['device'])
        context['section'] = '{device} apps'.format(device=device_name)
        return context
    
    def get_queryset(self):
        
        device = self.kwargs['device']
        
        return Application.objects.apps_by_device(device)

class SearchAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(SearchAppListView, self).get_context_data(**kwargs)
        context['section'] = self.request.GET.get("keyword", "")
        return context
    
    def get_queryset(self):
        keywords = self.request.GET.get("keyword", "")
        #TODO move to manager
        return Application.objects.filter(Q(title__search=keywords)).distinct()

class CategoryAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(CategoryAppListView, self).get_context_data(**kwargs)
        context['section'] = self.kwargs['category'] + ' apps'
        context['category'] = self.kwargs['category']
        return context
    
    def get_queryset(self):
        category = self.kwargs['category']
        return Application.objects.apps_by_category(category)

class ArtistAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(ArtistAppListView, self).get_context_data(**kwargs)
        artist = Artist.objects.get(id=int(self.kwargs['artist_id']))
        context['section'] = artist.name  + ' apps'
        return context
    
    def get_queryset(self):
        artist_id = int(self.kwargs['artist_id'])
        return Application.objects.apps_by_artist(artist_id)

class TopAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(TopAppListView, self).get_context_data(**kwargs)
        context['section'] = 'Top 100 apps'
        context['filter'] = 'top100'
        return context
    
    def get_queryset(self):
        return Application.objects.top_apps()

class TopCategoryAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(TopCategoryAppListView, self).get_context_data(**kwargs)
        context['section'] = 'Top {category} apps'.format(
                                            category=self.kwargs['category'])
        return context
    
    def get_queryset(self):
        return Application.objects.top_category_apps(self.kwargs['category'])

class AppsByRatingView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(AppsByRatingView, self).get_context_data(**kwargs)
        context['section'] = 'Best rated apps'
        context['filter'] = 'rating'
        return context
    
    def get_queryset(self):
        return Application.objects.apps_by_ratings()

class NewAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(NewAppListView, self).get_context_data(**kwargs)
        context['section'] = 'New apps'
        context['filter'] = 'new'
        return context
    
    def get_queryset(self):
        return Application.objects.new_apps()

class UpdateAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(UpdateAppListView, self).get_context_data(**kwargs)
        context['section'] = 'Updated apps'
        context['filter'] = 'updated'
        return context
    
    def get_queryset(self):
        return Application.objects.updated_apps()


class PaidAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(PaidAppListView, self).get_context_data(**kwargs)
        context['section'] = 'Paid apps'
        context['filter'] = 'paid'
        return context
    
    def get_queryset(self):
        return Application.objects.paid_apps()
    
class FreeAppListView(BaseAppListView):
    
    def get_context_data(self, **kwargs):
        
        context =  super(FreeAppListView, self).get_context_data(**kwargs)
        context['section'] = 'Free apps'
        context['filter'] = 'free'
        return context
    
    def get_queryset(self):
        return Application.objects.free_apps()


class AppDetailView(DetailView):
    template_name = "app_detail.html"
    model = Application
    context_object_name = 'app'
    
