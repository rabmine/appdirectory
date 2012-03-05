from django import template
from app.models import CATEGORIES, Application
from django.core.urlresolvers import reverse, NoReverseMatch
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
    
    top_apps = Application.objects.top_apps(1)[:10]
    
    return {'categories' : categories,
            'app_count' : app_count,
            'iphone_count' : iphone_count,
            'ipad_count' : ipad_count,
            'selected' : selected,
            'top_apps' : top_apps}

@register.filter
def detail_link(app):
    try:
        return reverse('app_detail_slug', args=(app.application_id, app.slug()))
    except NoReverseMatch:
        return reverse('app_detail', args=(app.application_id,))
