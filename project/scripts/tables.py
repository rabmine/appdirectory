'''
Scripts to update and create extra tables needed by the app.
'''

from settings import DATABASES
import MySQLdb
from app.constants import USA_STOREFRONT, OTHER_STOREFRONTS
from datetime import datetime, timedelta
import time

def save_artists(cursor):
    
    print "Saving artist table"
    
    cursor.execute("TRUNCATE TABLE app_artist")
    cursor.execute("TRUNCATE TABLE app_applicationartist")
    
    cursor.execute ("""INSERT IGNORE INTO app_artist (name) 
                    SELECT artist_name from epf_application""")
    
    cursor.execute ("""INSERT IGNORE INTO app_applicationartist 
                    (application_id, artist_id) 
                    SELECT epf_application.application_id, app_artist.id 
                    FROM epf_application LEFT JOIN app_artist ON
                    app_artist.name = epf_application.artist_name
                    """)


def save_new(cursor):
    
    print "Saving new apps table"
    
    TABLE_NAME = 'app_newapps'
    
    cursor.execute("TRUNCATE TABLE {table}".format(table=TABLE_NAME))
    
    cursor.execute("""INSERT INTO {table} (application_id) SELECT application_id
                    FROM epf_application WHERE itunes_release_date > %s"""
                    .format(table=TABLE_NAME), datetime.now())

def save_us_price(cursor):
    
    print "Saving US price table"
    
    US_TABLE_NAME = 'app_applicationpriceus'
    cursor.execute("TRUNCATE TABLE {table}".format(table=US_TABLE_NAME))
    cursor.execute("""INSERT INTO {table} (application_id, retail_price) 
                     SELECT application_id, retail_price FROM epf_application_price 
                     WHERE storefront_id={storefront} AND retail_price > 0"""
                    .format(table=US_TABLE_NAME, storefront=USA_STOREFRONT))
        
def save_other_price(cursor):
    
    print "Saving foreign price table"
    
    OTHER_TABLE_NAME = 'app_applicationpriceother'
    cursor.execute("TRUNCATE TABLE {table}".format(table=OTHER_TABLE_NAME))
    
    cursor.execute("""INSERT INTO {table} (application_id, storefront_id, retail_price) 
                     SELECT application_id, storefront_id, retail_price 
                     FROM epf_application_price 
                     WHERE storefront_id IN {storefront} AND retail_price > 0"""
                    .format(table=OTHER_TABLE_NAME, 
                            storefront=str(tuple(OTHER_STOREFRONTS.keys()))))

def save_pricedrop(cursor):
    
    print "Saving pricedrop table"
    
    TABLE_NAME = 'app_pricedrop'
    cursor.execute("TRUNCATE TABLE {table}".format(table=TABLE_NAME))
    cursor.execute("""INSERT INTO {table} (application_id, previous_price) 
                    SELECT app_applicationhistory.application_id, 
                    app_applicationhistory.retail_price FROM 
                    app_applicationhistory LEFT JOIN app_applicationpriceus
                    ON app_applicationhistory.application_id = app_applicationpriceus.application_id
                    WHERE app_applicationhistory.retail_price > app_applicationpriceus.retail_price"""
                    .format(table=TABLE_NAME))
    

def save_top100(cursor):
    
    print "Saving top100 table"
    
    TABLE_NAME = 'app_applicationpopularity'
    STOREFRONT = str(USA_STOREFRONT)
    
    cursor.execute("TRUNCATE TABLE {table}".format(table=TABLE_NAME))
    cursor.execute("""INSERT INTO {table} (application_id, genre_id, 
                    application_rank) SELECT application_id, genre_id, 
                    application_rank FROM epf_application_popularity_per_genre WHERE
                    storefront_id={storefront} AND application_rank <= 100"""
                    .format(table=TABLE_NAME, storefront=STOREFRONT))

def save_updated(cursor):
    
    print "Saving updated apps table"
    
    TABLE_NAME = 'app_updatedapps'
    
    cursor.execute("TRUNCATE TABLE {table}".format(table=TABLE_NAME))
    
    limit_date = datetime.today() - timedelta(days=15)
    timestamp = int(time.mktime(limit_date.timetuple()) * 1000)
    
    cursor.execute("""INSERT INTO {table} (application_id) SELECT application_id
                    FROM epf_application WHERE export_date > {timestamp}"""
                    .format(table=TABLE_NAME, timestamp=timestamp))


def run():
    conn = MySQLdb.connect (host = DATABASES['default']['HOST'],
                            user = DATABASES['default']['USER'],
                            passwd = DATABASES['default']['PASSWORD'],
                            db = DATABASES['default']['NAME'])
    cursor = conn.cursor ()

    save_us_price(cursor)
    save_other_price(cursor)
    save_artists(cursor)
    
    save_pricedrop(cursor)
    save_top100(cursor)
    save_new(cursor)
    save_updated(cursor)
        
    cursor.close()
    conn.close()

run()
