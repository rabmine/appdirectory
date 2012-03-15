'''
App activity graph.
'''
from django.views.generic.base import TemplateView
from django.http import HttpResponse
import json
from app.models import Application

class ActivityGraphView(TemplateView):
    """ Base class for activity graph views. """
    
    def get_data_points(self, app):
        return [['23-May-08', 578.55], ['20-Jun-08', 566.5], ['25-Jul-08', 480.88], ['22-Aug-08', 509.84],
                   ['26-Sep-08', 454.13], ['24-Oct-08', 379.75], ['21-Nov-08', 303], ['26-Dec-08', 308.56],
                   ['23-Jan-09', 299.14], ['20-Feb-09', 346.51], ['20-Mar-09', 325.99], ['24-nov-09', 386.15]]
    
    def get_yaxis_format(self):
        return ""
    
    def get_context_data(self, **kwargs):
        app_id=int(self.kwargs['app_id'])
        app = Application.objects.get(application_id=app_id)
        
        
        return {'data' : self.get_data_points(app),
                'yaxis_format' : self.get_yaxis_format()}
    
    def render_to_response(self, context):
        return HttpResponse(json.dumps(context),
                            content_type='application/json')


class PriceGraphView(ActivityGraphView):
    def get_yaxis_format(self):
        return "$%.2f"

class VersionGraphView(ActivityGraphView):
    pass

class Top250GraphView(ActivityGraphView):
    pass