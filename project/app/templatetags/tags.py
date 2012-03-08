from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
register = template.Library()

from django.core.cache import cache

@register.inclusion_tag('site/sidebar.html')
def sidebar(selected=None):
    
    keys = cache.get_many(['sb_categories', 'sb_app_count', 'sb_iphone_count', 
                           'sb_ipad_count', 'sb_top_apps'])
    
    return {'categories' : keys.get('sb_categories', []),
            'app_count' : keys.get('sb_app_count', ''),
            'iphone_count' : keys.get('sb_iphone_count', ''),
            'ipad_count' : keys.get('sb_ipad_count' , ''),
            'selected' : selected,
            'top_apps' : keys.get('sb_top_apps', [])}

@register.filter
def detail_link(app):
    try:
        return reverse('app_detail_slug', args=(app.application_id, app.slug()))
    except NoReverseMatch:
        return reverse('app_detail', args=(app.application_id,))
