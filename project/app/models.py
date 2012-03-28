from django.db import models
from appleutils import get_rating
from appleutils import affiliate_encode
from django.template.defaultfilters import slugify

from constants import *
from decimal import Decimal

class ApplicationManager(models.Manager):
    
    def apps_by_artist(self, artist_id):
        """ Returns the apps developed by the given artist. """
        
        return self.filter(applicationartist__artist__id=artist_id).distinct()
    
    def apps_by_category(self, category):
        ids = CATEGORIES[category]
        return self.filter(genreapplication__genre__genre_id__in=ids).distinct()
    
    def apps_by_device(self, device_name):
        """
        Returns apps for the given device (mac, ios, all, iphone, ipod, ipad). 
        """
        
        device_types = DEVICES[device_name]
        return self.filter(applicationdevicetype__device_type__device_type_id__in=
                           device_types).distinct()
    
    def top_category_apps(self, category):
        
        if CATEGORIES.has_key(category):
            genre_ids = CATEGORIES[category]
        else:
            genre_ids = Genre.objects.filter(name=category).values_list('genre_id', flat=True)
        
        return self.filter(applicationpopularity__isnull=False, 
                    applicationpopularity__genre__genre_id__in=genre_ids)
    
    def top_apps(self):
        """ Returns the apps in the top 100."""
        
        return self.filter(applicationpopularity__isnull=False)
    
    def price_drops(self):
        """ Returns the apps that have lowered its price since last import. """
        
        return self.filter(pricedrop__isnull=False)
        
    def paid_apps(self):
        return self.filter(applicationpriceus__isnull=False)
    
    def free_apps(self):
        return self.filter(applicationpriceus__isnull=True)
                           
    def new_apps(self):
        return self.filter(newapps__isnull=False)
    
    def updated_apps(self):
        return self.filter(updatedapps__isnull=False)
    
    def apps_by_ratings(self):
        return self.filter(applicationrating__count__gt=0).order_by(
                                                '-applicationrating__average')
    
class Application(models.Model):
    
    objects = ApplicationManager()
    
    export_date = models.BigIntegerField()
    application_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=3000, blank=True)
    view_url = models.CharField(max_length=3000, blank=True)
    artwork_url_large = models.CharField(max_length=3000, blank=True)
    itunes_release_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=300, blank=True)
    itunes_version = models.CharField(max_length=300, blank=True)
    download_size = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = u'epf_application'
        managed = False
    
    #FIXME use ids
    def _get_devices(self):
        device_names = self.applicationdevicetype_set.values_list('device_type__name', flat=True)
        device_types = ["iPhone", "iPad", "iPod" , "Mac", "All"]
        contains_device = lambda dev : len([x for x in device_names if x.startswith(dev)])
        return [device for device in device_types if contains_device(device)]
    
    def __unicode__(self):
        return self.title
    
    def slug(self):
        return slugify(self.title)
    
    def price(self, storefront_id):
        """ 
        Returns the retail price of the app in the given storefront or zero 
        if not found. 
        """
        
        if storefront_id == USA_STOREFRONT:
            price = self.applicationpriceus_set.all()
        else:
            price = self.applicationpriceother_set.filter(
                                            storefront_id=storefront_id)
        
        return price[0].retail_price if price else Decimal('0.0')
    
    def get_rating(self):
        #TODO should expire to get latest rating
        
        ratings = self.applicationrating_set.all()
        
        if not ratings:
            rating = ApplicationRating()
            rating.application = self
            rating.count, rating.average = get_rating(self.application_id)
            rating.save()
            return rating.average
        
        return ratings[0].average
        
    
    def affiliate_url(self):
        """ Returns the affiliate encoded version of the app's url. """
        
        return affiliate_encode(self.view_url)
    
    def get_artist(self):
        artist_id = self.applicationartist_set.all()[0].artist_id
        return Artist.objects.get(id=artist_id)
    
    def get_plattform(self):
        devices = self._get_devices()
        if len(devices) == 1:
            if devices[0] != "Mac" and devices[0] != "All":
                return "iOS " + devices[0]
            return devices[0]
        return None
    
    def get_category(self):
        genres = self.genreapplication_set.filter(is_primary=1).values_list('genre__name', flat=True)[:1]
        if not genres:
            genres = self.genreapplication_set.all().values_list('genre__name', flat=True)[:1]
        
        return genres[0] if genres else ''
    
    def get_devices(self):
        devices = self._get_devices()
        return " ".join(devices)
    
    def is_update(self):
        return self.updatedapps_set.count()
    
    def is_new(self):
        return self.newapps_set.count()
    
    def pricedrop(self):
        """ 
        If this app is a pricedrop returns the pevious price, otherwise 
        returns None. 
        """
        
        qs = self.pricedrop_set.all()
        return '$%.2f' % (qs[0].previous_price,) if qs else None
    
    def rank(self):
        """ Returns the rank of the app. """
        
        qs = self.applicationpopularity_set.all()
        return qs[0].application_rank if qs else None 
    
    def is_top100(self):
        """ Returns True if this app is top 100. """
        
        return self.applicationpopularity_set.count()
    
    def get_languages(self):
        codes = list(self.applicationdetail_set.values_list('language_code', flat=True))
        return [LANGUAGE_CODES[c.lower()] for c in codes]
    
    def detail(self):
        return self.applicationdetail_set.all()[0]
        

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
    ipad_screenshot_url_1 = models.CharField(max_length=3000, blank=True)
    ipad_screenshot_url_2 = models.CharField(max_length=3000, blank=True)
    ipad_screenshot_url_3 = models.CharField(max_length=3000, blank=True)
    ipad_screenshot_url_4 = models.CharField(max_length=3000, blank=True)
    ipad_screenshot_width_height_1 = models.CharField(max_length=60, blank=True)
    ipad_screenshot_width_height_2 = models.CharField(max_length=60, blank=True)
    ipad_screenshot_width_height_3 = models.CharField(max_length=60, blank=True)
    ipad_screenshot_width_height_4 = models.CharField(max_length=60, blank=True)
    
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

""" CUSTOM TABLES """
        
class ApplicationRating(models.Model):
    application = models.ForeignKey(Application, unique=True)
    average = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    count = models.BigIntegerField(default=0)
    saved = models.DateTimeField(auto_now=True)

class Artist(models.Model):
    name = models.CharField(max_length=160, blank=True, unique=True)
    
    def app_count(self):
        """ Returns the amount of apps by this artist. """
        
        return self.applicationartist_set.all().count()

class ApplicationArtist(models.Model):
    application = models.ForeignKey(Application)
    artist = models.ForeignKey(Artist)
    
    class Meta:
        unique_together = ('application', 'artist')
    
class ApplicationPriceUS(models.Model):
    application = models.ForeignKey(Application, unique=True)
    retail_price = models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True)

class ApplicationPriceOther(models.Model):
    application = models.ForeignKey(Application)
    retail_price = models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True)
    storefront_id = models.IntegerField()
    
    class Meta:
        unique_together = ('application', 'storefront_id')
    

class ApplicationPopularity(models.Model):
    application = models.ForeignKey(Application)
    genre = models.ForeignKey(Genre)
    application_rank = models.IntegerField()
    
    class Meta:
        unique_together = ('application', 'genre')

class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application)
    export_date = models.BigIntegerField()
    
    version = models.CharField(max_length=300, blank=True)
    retail_price = models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True)
    application_rank = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ('application', 'export_date')

class PriceDrop(models.Model):
    application = models.ForeignKey(Application)
    previous_price = models.DecimalField(null=True, max_digits=9, decimal_places=3, blank=True)
    
class UpdatedApps(models.Model):
    application = models.ForeignKey(Application)

class NewApps(models.Model):
    application = models.ForeignKey(Application)
