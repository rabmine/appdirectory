'''
Helper functions to interact with apple apis.
'''
import requests
import json
from decimal import Decimal
import urlparse
import urllib

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


AFFILIATE_URL = 'http://click.linksynergy.com/fs-bin/stat?id=6QoH5MQGNgI&offerid=146261&type=3&subid=0&tmpid=1826&RD_PARM1='
def _append_partner(url):
    
    if urlparse.urlparse(url)[4]:
        return url + '&partnerId=30'
    else:
        return url + '?partnerId=30'
    
def affiliate_encode(url):
    """ Takes a raw itunes link and encodes it to use affiliate information. """
    
    url = _append_partner(url)
    return AFFILIATE_URL + urllib.quote(urllib.quote(url, ''))
 