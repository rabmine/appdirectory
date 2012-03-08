'''
Script that traverses the applications table and populates the artist and 
application_artist tables.
'''
from settings import DATABASES
import MySQLdb
from app.models import USA_STOREFRONT
from decimal import Decimal

STOREFRONT = str(USA_STOREFRONT)
TABLE_NAME = 'app_applicationpriceus'

def save_app_price(cursor, application_id):
    cursor.execute ("""SELECT retail_price FROM epf_application_price 
                        WHERE application_id=%s AND storefront_id=%s""", 
                        (application_id, STOREFRONT))
    
    
    row = cursor.fetchone()
    if row and Decimal(row[0]):
        cursor.execute("""INSERT INTO {table} (application_id, retail_price) 
                        VALUES (%s, %s) ON DUPLICATE KEY UPDATE 
                        retail_price=%s""".format(table=TABLE_NAME),
                        (application_id, row[0], row[0]))
    else:
        cursor.execute("""DELETE FROM {table} 
                        WHERE application_id=%s""".format(table=TABLE_NAME),
                        application_id)

def save_prices(cursor):
    cursor.execute ("SELECT application_id FROM epf_application")
    for row in cursor.fetchall():
        save_app_price(cursor, row[0])
        
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