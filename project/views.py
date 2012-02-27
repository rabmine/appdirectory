from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "index.html"

class AppDetailView(TemplateView):
    template_name = "app_detail.html"
