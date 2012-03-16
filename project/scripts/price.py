'''
Script that traverses the applications table and populates the artist and 
application_artist tables.
'''
from project.settings import DATABASES
import MySQLdb
from app.constants import USA_STOREFRONT, OTHER_STOREFRONTS

US_TABLE_NAME = 'app_applicationpriceus'
OTHER_TABLE_NAME = 'app_applicationpriceother'


def save_us_price(cursor):
    cursor.execute("TRUNCATE TABLE {table}".format(table=US_TABLE_NAME))
    cursor.execute("""INSERT INTO {table} (application_id, retail_price) 
                     SELECT application_id, retail_price FROM epf_application_price 
                     WHERE storefront_id={storefront} AND retail_price > 0"""
                    .format(table=US_TABLE_NAME, storefront=USA_STOREFRONT))
        
def save_other_price(cursor):
    cursor.execute("TRUNCATE TABLE {table}".format(table=OTHER_TABLE_NAME))
    
    cursor.execute("""INSERT INTO {table} (application_id, storefront_id, retail_price) 
                     SELECT application_id, storefront_id, retail_price 
                     FROM epf_application_price 
                     WHERE storefront_id IN {storefront} AND retail_price > 0"""
                    .format(table=OTHER_TABLE_NAME, 
                            storefront=str(tuple(OTHER_STOREFRONTS.keys()))))

def save_prices(cursor):
    save_us_price(cursor)
    save_other_price(cursor)
        
def run():
    conn = MySQLdb.connect (host = DATABASES['default']['HOST'],
                            user = DATABASES['default']['USER'],
                            passwd = DATABASES['default']['PASSWORD'],
                            db = DATABASES['default']['NAME'])
    cursor = conn.cursor ()

    save_prices(cursor)
        
    cursor.close()
    conn.close()

run()