'''
App activity graph.
'''
from django.views.generic.base import TemplateView
from django.http import HttpResponse
import json
from app.models import Application
from app.constants import USA_STOREFRONT

class ActivityGraphView(TemplateView):
    """ Base class for activity graph views. """
    
    def get_yaxis_format(self):
        return ""
    
    def patch_max(self, context):
        """ 
        Checks if all y points are equal, and adds a max flag to avoid jqplot
        drawing a constant line at the top of the graph.
        """
        
        if context['data']:
            value = context['data'][0][1]
            constant = True
            
            for _, v in context['data']:
                if v != value:
                    constant = False
                    break
        
            if constant:
                context.update({'max' : value * 2 })
    
    def get_context_data(self, **kwargs):
        app_id=int(self.kwargs['app_id'])
        app = Application.objects.get(application_id=app_id)
        
        context = {'data' : self.get_data_points(app),
                   'yaxis_format' : self.get_yaxis_format()}
        
        self.patch_max(context)
        
        return context
    
    def render_to_response(self, context):
        return HttpResponse(json.dumps(context),
                            content_type='application/json')


class PriceGraphView(ActivityGraphView):
    
    def get_data_points(self, app):
        values = app.applicationhistory_set.values_list('export_date', 'retail_price')
        
        points = [[date, float(str(price))] for date, price in values]
        points.append([app.export_date, float(str(app.price(USA_STOREFRONT)))])
        
        return points
    
    def get_yaxis_format(self):
        return "$%.2f"

class VersionGraphView(ActivityGraphView):
    pass

class Top250GraphView(ActivityGraphView):
    pass