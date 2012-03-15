'''
App activity graph.
'''
from django.views.generic.base import TemplateView
from django.http import HttpResponse
import json
from app.models import Application
from app.constants import USA_STOREFRONT
import time

class ActivityGraphView(TemplateView):
    """ Base class for activity graph views. """
    
    def now_timestamp(self):
        return time.time() * 1000
    
    def get_yaxis(self):
        return {}
    
    def get_context_data(self, **kwargs):
        app_id=int(self.kwargs['app_id'])
        app = Application.objects.get(application_id=app_id)
        
        data = self.get_data_points(app)
        
        context = {'data' : data,
                   'title' : self.get_title(),
                   'yaxis' : self.get_yaxis(data)}
        
        return context
    
    def render_to_response(self, context):
        return HttpResponse(json.dumps(context),
                            content_type='application/json')


class PriceGraphView(ActivityGraphView):
    
    def get_title(self):
        return "App price"
    
    def get_data_points(self, app):
        values = app.applicationhistory_set.values_list('export_date', 'retail_price')
        
        points = [[date, float(str(price)) if price else 0]
                   for date, price in values]
        
        price = app.price(USA_STOREFRONT)
        if price:
            points.append([self.now_timestamp(), float(str(price)) if price else 0])
        
        return points
    
    def patch_max(self, data):
        """ 
        Checks if all y points are equal, and adds a max flag to avoid jqplot
        drawing a constant line at the top of the graph.
        """
        
        if data:
            value = data[0][1]
            for _, v in data:
                if v != value:
                    return False
        
            return True
    
    
    def get_yaxis(self, data):
        
        yaxis = {'tickOptions': {
                                'formatString' : "$%.2f",
                                }
                }
        
        if self.patch_max(data):
            yaxis['max'] = data[0][1] * 2
            yaxis['min'] = 0
        
        return yaxis

class VersionGraphView(ActivityGraphView):
    
    def get_title(self):
        return "Version"
    

class Top250GraphView(ActivityGraphView):
    
    def get_title(self):
        return "Top 250"
    
    def get_yaxis(self, data):
        return {'max' : 1, 'min' : 250,
                'tickOptions': {
                                'formatString' : "#%d",
                                }}
    
    def get_data_points(self, app):
        values = app.applicationhistory_set.values_list('export_date', 'application_rank')
        points = [[date, rank] for date, rank in values]
        
        current_rank = app.rank()
        if current_rank and current_rank <= 250:
            points.append([self.now_timestamp(), current_rank])
        
        return points