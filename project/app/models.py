from django.db import models

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


class Application(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    application_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=3000, blank=True)
    recommended_age = models.CharField(max_length=60, blank=True)
    artist_name = models.CharField(max_length=3000, blank=True)
    seller_name = models.CharField(max_length=3000, blank=True)
    company_url = models.CharField(max_length=3000, blank=True)
    support_url = models.CharField(max_length=3000, blank=True)
    view_url = models.CharField(max_length=3000, blank=True)
    artwork_url_large = models.CharField(max_length=3000, blank=True)
    artwork_url_small = models.CharField(max_length=3000, blank=True)
    itunes_release_date = models.DateTimeField(null=True, blank=True)
    copyright = models.CharField(max_length=12000, blank=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=300, blank=True)
    itunes_version = models.CharField(max_length=300, blank=True)
    download_size = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table = u'epf_application'
        managed = False
    
    def _get_devices(self):
        application_devices = ApplicationDeviceType.objects.filter(application_id=self.application_id)
        device_names = [application_device.device_type.name for application_device in application_devices ]
        device_types = ["iPhone", "iPad", "iPod" , "Mac", "All"]
        contains_device = lambda dev : len([x for x in device_names if x.startswith(dev)])
        return [device for device in device_types if contains_device(device)]
    
    def _str_(self):
        return self.title
    
    def __unicode__(self):
        return self.title
    
    def __repr__(self):
        return self.title
    
    def is_pricedrop(self):
        return False
    
    def price(self):
        try:
            application_prices = ApplicationPrice.objects.filter(application_id=self.application_id)
            retail_price = application_prices[0].retail_price
        except:
            retail_price = 0
        return '$' + str(round(retail_price,2))
    
    def get_previous_price(self):
        return None
    
    def get_artist_app_count(self):
        return len(Application.objects.filter(artist_name=self.artist_name))
    
    def get_plattform(self):
        devices = self._get_devices()
        if len(devices) == 1:
            if devices[0] != "Mac" and devices[0] != "All":
                return "iOS " + devices[0]
            return devices[0]
        return None
    
    def get_category(self):
        genres = GenreApplication.objects.filter(application_id=self.application_id)
        return genres[0].genre.name
    
    def get_devices(self):
        devices = self._get_devices()
        return ", ".join(devices)
        
    def is_top100(self):
        return False    

class ApplicationDetail(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    application = models.ForeignKey(Application)
    application_id = models.IntegerField(primary_key=True)
    language_code = models.CharField(max_length=60)
    title = models.CharField(max_length=3000, blank=True)
    description = models.TextField(blank=True)
    release_notes = models.TextField(blank=True)
    company_url = models.CharField(max_length=3000, blank=True)
    support_url = models.CharField(max_length=3000, blank=True)
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

class ApplicationPopularityPerGenre(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    storefront_id = models.IntegerField(primary_key=True)
    genre_id = models.IntegerField(primary_key=True)
    application_id = models.IntegerField(primary_key=True)
    application = models.ForeignKey(Application)
    application_rank = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'epf_application_popularity_per_genre'
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
    class Meta:
        db_table = u'epf_genre_application'
        managed = False

class ApplicationPrice(models.Model):
    export_date = models.BigIntegerField(null=True, blank=True)
    application_id = models.IntegerField(primary_key=True)
    retail_price = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    currency_code = models.CharField(max_length=60, blank=True)
    storefront_id = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'epf_application_price'
        managed = False
