APPS_PER_PAGE = 20

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView

from models import Application, ApplicationDeviceType, DeviceType

class HomeView(TemplateView):
    template_name = "index.html"

class AppDetailView(TemplateView):
    template_name = "app_detail.html"
    
def execute_query(query):
    cursor = connection.cursor()
    row_count = cursor.execute(query)
    for _ in xrange(row_count):
        yield cursor.fetchone()

def update_view_data(request, view_data):
    view_data["selected_page"] = int(request.GET.get("page", 1))
    view_data["available_apps"] = Application.objects.all().count()
    
    page_range = xrange(1,11)
    page_info = {}
    
    for pr in page_range:
        page_info[pr] = False
    
    selected_page = view_data["selected_page"]
    page_info[selected_page] = True
    
    view_data["page_info"] = page_info
    view_data["last_page"] = page_range[-1] + 1

def _get_applications(platform, type="all",params=None):
    params = params or {}
    page = int(params.get("page", 1))
    page_length = settings.RESULTS_PAGE_LENGTH
    skip = (page-1)*(page_length)
    
    if platform == "ios":
        if type == "all":
            device_types = DeviceType.objects.exclude(name__icontains="mac")
        else:
            device_types = DeviceType.objects.filter(name__icontains=type)  
    elif platform == "mac":
        device_types = DeviceType.objects.filter(name__icontains="mac")
    
    device_type_ids = [str(dt.device_type_id) for dt in device_types]
    dev_types = "(" + ",".join(device_type_ids) + ")"
    
    query = """SELECT application_id 
    FROM epf_application_device_type
    WHERE  device_type_id in %p
    GROUP BY application_id LIMIT %s OFFSET %s""".replace("%p", dev_types)
 
    application_ids = [int(appdev[0]) for appdev in execute_query(query % (page_length, skip))]   
    result_apps = Application.objects.filter(application_id__in=application_ids)

    return result_apps

def _search(application, keywords):
    query = Q(title__search=keywords) | Q(description__search=keywords)
    return application.filter(query)
    
def home(request):
    applications = _get_applications("ios", params=request.GET)
    view_data = dict(applications=applications,area="ios")
    update_view_data(request, view_data)
    return render_to_response("index.html", view_data)
    
def ios(request):
    return HttpResponseRedirect(reverse())

def iphone(request):
    applications = _get_applications("ios", "iphone", params=request.GET)
    view_data = dict(applications=applications,area="iphone")
    update_view_data(request, view_data)
    return render_to_response("index.html", view_data)

def ipad(request):
    applications = _get_applications("ios", "ipad", params=request.GET)
    view_data = dict(applications=applications,area="ipad")
    update_view_data(request, view_data)
    return render_to_response("index.html", view_data)

def ipod(request):
    applications = _get_applications("ios", "ipod", params=request.GET)
    view_data = dict(applications=applications,area="ipod")
    update_view_data(request, view_data)
    return render_to_response("index.html", view_data)

def mac(request):
    applications = _get_applications("mac", params=request.GET)
    view_data = dict(applications=applications,area="mac")
    update_view_data(request, view_data)
    return render_to_response("index.html", view_data)

def search(request):
    keywords = request.GET.get("q", "")
    applications = _search(Application.objects.all(), keywords)
    view_data = dict(applications=applications)
    update_view_data(request, view_data)
    return render_to_response("index.html",view_data)

def artist_applications(request, artist_name):
    artist_applications = Application.objects.filter(artist_name=artist_name)[:APPS_PER_PAGE]
    view_data = dict(applications=artist_applications)
    update_view_data(request, view_data)
    return render_to_response("index.html", view_data)

def detail(request, id):
    application = get_object_or_404(Application, application_id=id)
    view_data = dict(app=application)
    return render_to_response("app_detail.html", view_data)
