'''
Helper functions to interact with apple search api.
'''
import requests
import json
from decimal import Decimal

ITUNES_URL = 'http://itunes.apple.com/lookup?id={app_id}'

def get_rating(application_id):
    """ Returns rating count and average for the given app id. """

    url = ITUNES_URL.format(app_id=application_id)
    response = json.loads(requests.get(url).text)
    
    try:
        results = response['results'][0]
        count = int(results.get('userRatingCount', 0))
        average = Decimal(str(results.get('averageUserRating', 0.0))) 
        
        return count, average
    
    except (KeyError, IndexError):
        return 0, Decimal('0.0') 