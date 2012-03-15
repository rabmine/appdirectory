from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from app.templatetags.truncate import truncatechars
from app.constants import USA_STOREFRONT, OTHER_STOREFRONTS

register = template.Library()

from django.core.cache import cache

@register.inclusion_tag('site/sidebar.html')
def sidebar(selected=None):
    keys = cache.get_many(['sb_categories', 'sb_app_count', 'sb_iphone_count', 
                           'sb_ipad_count', 'sb_top_apps', 'sb_ipod_count'])
    
    return {'categories' : keys.get('sb_categories', []),
            'app_count' : keys.get('sb_app_count', ''),
            'iphone_count' : keys.get('sb_iphone_count', ''),
            'ipad_count' : keys.get('sb_ipad_count' , ''),
            'ipod_count' : keys.get('sb_ipod_count' , ''),
            'selected' : selected,
            'top_apps' : keys.get('sb_top_apps', [])}

@register.inclusion_tag('site/currencies.html')
def currencies(request):
    
    selected = request.session.get('storefront')
    
    return {'USA' : USA_STOREFRONT,
            'OTHER' : OTHER_STOREFRONTS, 
            'selected' : selected}

@register.filter
def price(app, request):
    sf = request.session.get('storefront', USA_STOREFRONT)
    
    currency = OTHER_STOREFRONTS[sf][1] + ' ' if sf != USA_STOREFRONT else '$'
    price = app.price(sf)
    return '%s%.2f' % (currency, price) if price else 'FREE'

@register.filter
def detail_link(app):
    try:
        return reverse('app_detail_slug', args=(app.application_id, app.slug()))
    except NoReverseMatch:
        return reverse('app_detail', args=(app.application_id,))

@register.filter
def category(app):
    category = app.get_category()
    if len(category) < 15:
        return "Category: " + category
    
    return category

@register.filter
def description(app):
    return truncatechars(app.description.encode('ascii', 'ignore'), 138)
    