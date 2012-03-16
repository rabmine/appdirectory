'''
Script to save historic information to the database before updating it.
'''

from project.settings import DATABASES
import MySQLdb
import time
from app.constants import USA_STOREFRONT

def save_history(cursor):
    date = time.time() * 1000
    cursor.execute("""INSERT INTO app_applicationhistory (application_id,
                    export_date, version) SELECT application_id, {date}, 
                    version FROM epf_application""".format(date=date))

    cursor.execute("""INSERT INTO app_applicationhistory (application_id, 
                    export_date, retail_price) SELECT application_id, {date}, 
                    retail_price FROM app_applicationpriceus
                    ON DUPLICATE KEY UPDATE 
                    retail_price=app_applicationpriceus.retail_price"""
                    .format(date=date))
    
    cursor.execute("""INSERT INTO app_applicationhistory (application_id, 
                    export_date, application_rank) SELECT application_id, {date}, 
                    application_rank FROM epf_application_popularity_per_genre
                    WHERE storefront_id={storefront} 
                    AND application_rank <= 250 ON DUPLICATE KEY UPDATE 
                    application_rank=epf_application_popularity_per_genre.application_rank"""
                    .format(date=date, storefront=USA_STOREFRONT))  

def run():
    conn = MySQLdb.connect (host = DATABASES['default']['HOST'],
                            user = DATABASES['default']['USER'],
                            passwd = DATABASES['default']['PASSWORD'],
                            db = DATABASES['default']['NAME'])
    cursor = conn.cursor ()

    save_history(cursor)
        
    cursor.close()
    conn.close()

run()
