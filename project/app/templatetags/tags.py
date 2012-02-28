from django import template
from app.models import CATEGORIES, Application

register = template.Library()

@register.inclusion_tag('site/sidebar.html')
def sidebar(selected=None):
    
    app_count = Application.objects.count()
    iphone_count = Application.objects.apps_by_device('iphone').count()
    ipad_count = Application.objects.apps_by_device('ipad').count()
    
    categories = []
    for category in CATEGORIES:
        count = Application.objects.apps_by_category(category).count()
        categories.append((category, count))
    
    
    return {'categories' : categories,
            'app_count' : app_count,
            'iphone_count' : iphone_count,
            'ipad_count' : ipad_count,
            'selected' : selected}