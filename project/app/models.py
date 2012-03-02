from django.db import models
from searchapi import get_rating
from decimal import Decimal
from datetime import datetime, timedelta
import time
from appleutils import affiliate_encode

CURRENCY_CODES = (('aus', 'Australia'),
                    ('aut', 'Austria'),
                    ('bel', 'Belgium'),
                    ('can', 'Canada'),
                    ('dnk', 'Denmark'),
                    ('fin', 'Finland'),
                    ('fra', 'France'),
                    ('deu', 'Germany'),
                    ('grc', 'Greece'),
                    ('irl', 'Ireland'),
                    ('ita', 'Italy'),
                    ('jpn', 'Japan'),
                    ('lux', 'Luxembourg'),
                    ('mex', 'Mexico'),
                    ('nld', 'Netherlands'),
                    ('nzl', 'New Zealand'),
                    ('nor', 'Norway'),
                    ('prt', 'Portugal'),
                    ('esp', 'Spain'),
                    ('swe', 'Sweden'),
                    ('che', 'Switzerland'),
                    ('gbr', 'United Kingdom'),
                    ('usa', 'United States'),)

CATEGORIES = (  'Book',
                'Business',
                'Education',
                'Entertainment',
                'Finance',
                'Games', 
                'Healthcare & Fitness',
                'Lifestyle',
                'Medical',
                'Music',
                'Navigation',
                'News',
                'Photography',
                'Productivity',
                'Reference',
                'Social Networking',
                'Sports',
                'Travel',
                'Utilities')

USA_STOREFRONT = 143441

class ApplicationManager(models.Manager):
    
#    def get_query_set(self):
#        return super(ApplicationManager, self).get_query_set().filter(
#                                        applicationdetail__language_code='EN').distinct()
    
    def apps_by_category(self, category):
        return self.filter(genreapplication__genre__name=category).distinct()
    
    def apps_by_device(self, device_name):
        """
        Returns apps for the given device (mac, ios, all, iphone, ipod, ipad). 
        """
        
        if device_name == "ios":
            device_types = DeviceType.objects.exclude(name__istartswith="mac")
  
        else:
            device_types = DeviceType.objects.filter(name__istartswith=device_name)
        
        return self.filter(applicationdevicetype__device_type__in=device_types
                                                    ).distinct()
    
    def top_apps(self, max_rank=100):
        """ Returns the apps in the top <max_rank>."""
        
        popular_categories = ('Games', 'Entertainment', 'Sports', 
                              'Social Networking', 
                              'Education', 'Music', 'News')
        
        apps = self.filter(genreapplication__genre__name__in=
                           popular_categories)
        
        return apps.filter(applicationpopularity__application_rank__lte=
                                max_rank, applicationpopularity__storefront_id=
                                USA_STOREFRONT).distinct()
                                
    def paid_apps(self):
        return self.filter(applicationprice__storefront_id=USA_STOREFRONT
                           ).exclude(applicationprice__retail_price=
                                     Decimal('0.0'))
    
    def free_apps(self):
        return self.filter(applicationprice__storefront_id=USA_STOREFRONT,
                           applicationprice__retail_price=Decimal('0.0'))
                           
    def new_apps(self):
        limit_date = datetime.today() - timedelta(days=7)
        return self.filter(itunes_release_date__gt=limit_date)
    
    def updated_apps(self):
        limit_date = datetime.today() - timedelta(days=7)
        timestamp = int(time.mktime(limit_date.timetuple()) * 1000)
        return self.filter(export_date__gt=timestamp)
    
    def apps_by_ratings(self):
        return self.filter(applicationrating__count__gt=0).order_by(
                                                '-applicationrating__average')

class Application(models.Model):
    
    objects = ApplicationManager()
    
    export_date = models.BigIntegerField(null=True, blank=True)
    application_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=3000, blank=True)
    #recommended_age = models.CharField(max_length=60, blank=True)
    artist_name = models.CharField(max_length=3000, blank=True)
    #seller_name = models.CharField(max_length=3000, blank=True)
    #company_url = models.CharField(max_length=3000, blank=True)
    #support_url = models.CharField(max_length=3000, blank=True)
    view_url = models.CharField(max_length=3000, blank=True)
    artwork_url_large = models.CharField(max_length=3000, blank=True)
    #artwork_url_small = models.CharField(max_length=3000, blank=True)
    itunes_release_date = models.DateTimeField(null=True, blank=True)
    #copyright = models.CharField(max_length=12000, blank=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=300, blank=True)
    itunes_version = models.CharField(max_length=300, blank=True)
    download_size = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = u'epf_application'
        managed = False
    
    def _get_devices(self):
        device_names = self.applicationdevicetype_set.values_list('device_type__name', flat=True)
        device_types = ["iPhone", "iPad", "iPod" , "Mac", "All"]
        contains_device = lambda dev : len([x for x in device_names if x.startswith(dev)])
        return [device for device in device_types if contains_device(device)]
    
    def _str_(self):
        return self.title
    
    def __unicode__(self):
        return self.title
    
    def __repr__(self):
        return self.title
    
    def price(self):
        retail_price = self.applicationprice_set.get(storefront_id=USA_STOREFRONT).retail_price
        return '$%.2f' % (retail_price,)
    
    def get_previous_price(self):
        return None
    
    def get_rating(self):
        rating, created = ApplicationRating.objects.get_or_create(
                                                    application=self)
        
        #TODO do it if expired too
        if created:
            rating.count, rating.average = get_rating(self.application_id)
            rating.save()
        
        return rating.average
    
    def affiliate_url(self):
        """ Returns the affiliate encoded version of the app's url. """
        
        return affiliate_encode(self.view_url)
    
    def get_artist_app_count(self):
        return Application.objects.filter(artist_name=self.artist_name).count()
    
    def get_plattform(self):
        devices = self._get_devices()
        if len(devices) == 1:
            if devices[0] != "Mac" and devices[0] != "All":
                return "iOS " + devices[0]
            return devices[0]
        return None
    
    def get_category(self):
        genres = self.genreapplication_set.filter(is_primary=1)
        if not genres:
            genres = self.genreapplication_set.all()
        
        return genres[0].genre.name if genres else ''
    
    def get_devices(self):
        devices = self._get_devices()
        return " ".join(devices)
    
    def is_update(self):
        today = datetime.today()
        export_date = datetime.fromtimestamp(self.export_date/1000)
        return today - export_date < timedelta(days=7)
    
    def is_pricedrop(self):
        return False
    
    def is_top100(self):
        return ApplicationPopularity.objects.filter(application=self, application_rank__lte=100,
                                                    storefront_id=USA_STOREFRONT).count()

class ApplicationDetail(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    application_id = models.IntegerField(primary_key=True)
    language_code = models.CharField(max_length=60)
#    title = models.CharField(max_length=3000, blank=True)
#    description = models.TextField(blank=True)
#    release_notes = models.TextField(blank=True)
#    company_url = models.CharField(max_length=3000, blank=True)
#    support_url = models.CharField(max_length=3000, blank=True)
    screenshot_url_1 = models.CharField(max_length=3000, blank=True)
    screenshot_url_2 = models.CharField(max_length=3000, blank=True)
    screenshot_url_3 = models.CharField(max_length=3000, blank=True)
    screenshot_url_4 = models.CharField(max_length=3000, blank=True)
    screenshot_width_height_1 = models.CharField(max_length=60, blank=True)
    screenshot_width_height_2 = models.CharField(max_length=60, blank=True)
    screenshot_width_height_3 = models.CharField(max_length=60, blank=True)
    screenshot_width_height_4 = models.CharField(max_length=60, blank=True)
#    ipad_screenshot_url_1 = models.CharField(max_length=3000, blank=True)
#    ipad_screenshot_url_2 = models.CharField(max_length=3000, blank=True)
#    ipad_screenshot_url_3 = models.CharField(max_length=3000, blank=True)
#    ipad_screenshot_url_4 = models.CharField(max_length=3000, blank=True)
#    ipad_screenshot_width_height_1 = models.CharField(max_length=60, blank=True)
#    ipad_screenshot_width_height_2 = models.CharField(max_length=60, blank=True)
#    ipad_screenshot_width_height_3 = models.CharField(max_length=60, blank=True)
#    ipad_screenshot_width_height_4 = models.CharField(max_length=60, blank=True)
    
    application = models.ForeignKey(Application)
    class Meta:
        db_table = u'epf_application_detail'
        managed = False

class ApplicationDeviceType(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    application_id = models.IntegerField(primary_key=True)
    device_type_id = models.IntegerField(primary_key=True)
    application = models.ForeignKey(Application)
    device_type = models.ForeignKey('DeviceType')
    class Meta:
        db_table = u'epf_application_device_type'
        managed = False

class ArtistApplication(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    artist_id = models.IntegerField(primary_key=True)
    application_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'epf_artist_application'
        managed = False

class DeviceType(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    device_type_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=600, blank=True)
    class Meta:
        db_table = u'epf_device_type'
        managed = False

class Genre(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    genre_id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=600, blank=True)
    class Meta:
        db_table = u'epf_genre'
        managed = False

class GenreApplication(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    genre_id = models.IntegerField(primary_key=True)
    application_id = models.IntegerField(primary_key=True)
    is_primary = models.IntegerField(null=True, blank=True)
    genre = models.ForeignKey(Genre)
    application = models.ForeignKey(Application)
    class Meta:
        db_table = u'epf_genre_application'
        managed = False

class ApplicationPrice(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    application_id = models.IntegerField(primary_key=True)
    retail_price = models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True)
    currency_code = models.CharField(max_length=20, blank=True)
    storefront_id = models.IntegerField(primary_key=True)
    
    application = models.ForeignKey(Application)
    class Meta:
        db_table = u'epf_application_price'
        managed = False

class ApplicationPopularity(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    storefront_id = models.IntegerField(primary_key=True)
    genre_id = models.IntegerField(primary_key=True)
    application_id = models.IntegerField(primary_key=True)
    application_rank = models.IntegerField()
    
    application = models.ForeignKey(Application)
    genre = models.ForeignKey(Genre)
    
    class Meta:
        db_table = u'epf_application_popularity_per_genre'
        managed = False
        
""" CUSTOM TABLES """
        
class ApplicationRating(models.Model):
    application = models.ForeignKey(Application)
    average = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    count = models.BigIntegerField(default=0)
    saved = models.DateTimeField(auto_now=True)

    
