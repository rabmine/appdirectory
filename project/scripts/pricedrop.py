'''
Creates a table with current pricedrops.
'''
from settings import DATABASES
import MySQLdb

TABLE_NAME = 'app_pricedrop'

def save_pricedrop(cursor):
    cursor.execute("TRUNCATE TABLE {table}".format(table=TABLE_NAME))
    cursor.execute("""INSERT INTO {table} (application_id, previous_price) 
                    SELECT app_applicationhistory.application_id, 
                    app_applicationhistory.retail_price FROM 
                    app_applicationhistory LEFT JOIN app_applicationpriceus
                    ON app_applicationhistory.application_id = app_applicationpriceus.application_id
                    WHERE app_applicationhistory.retail_price > app_applicationpriceus.retail_price"""
                    .format(table=TABLE_NAME))

def run():
    conn = MySQLdb.connect (host = DATABASES['default']['HOST'],
                            user = DATABASES['default']['USER'],
                            passwd = DATABASES['default']['PASSWORD'],
                            db = DATABASES['default']['NAME'])
    cursor = conn.cursor ()

    save_pricedrop(cursor)
        
    cursor.close()
    conn.close()

run()