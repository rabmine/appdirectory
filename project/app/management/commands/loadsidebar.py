'''
Command to load in cache the data used by the sidebar to avoid making querys 
on page load.
'''
from django.core.management.base import NoArgsCommand
from app.models import Application
from app.constants import CATEGORIES

from django.core.cache import cache

TIMEOUT = 604800 #a week

class Command(NoArgsCommand):
    
    def handle_noargs(self, **options):
        
        keys = {}
        keys['sb_app_count'] = Application.objects.count()
        keys['sb_iphone_count'] = Application.objects.apps_by_device('iphone').count()
        keys['sb_ipad_count'] = Application.objects.apps_by_device('ipad').count()
        
        categories = []
        for category in CATEGORIES:
            count = Application.objects.apps_by_category(category).count()
            categories.append((category, count))
        
        keys['sb_categories'] = categories
        
        cache.set_many(keys, TIMEOUT)
        