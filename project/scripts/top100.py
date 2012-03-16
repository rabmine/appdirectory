'''
Creates a table with the top100
'''
from project.settings import DATABASES
import MySQLdb
from app.constants import USA_STOREFRONT

TABLE_NAME = 'app_applicationpopularity'
STOREFRONT = str(USA_STOREFRONT)

def save_top100(cursor):
    cursor.execute("TRUNCATE TABLE {table}".format(table=TABLE_NAME))
    cursor.execute("""INSERT INTO {table} (application_id, genre_id, 
                    application_rank) SELECT application_id, genre_id, 
                    application_rank FROM epf_application_popularity_per_genre WHERE
                    storefront_id={storefront} AND application_rank <= 100"""
                    .format(table=TABLE_NAME, storefront=STOREFRONT))

def run():
    conn = MySQLdb.connect (host = DATABASES['default']['HOST'],
                            user = DATABASES['default']['USER'],
                            passwd = DATABASES['default']['PASSWORD'],
                            db = DATABASES['default']['NAME'])
    cursor = conn.cursor ()

    save_top100(cursor)
        
    cursor.close()
    conn.close()

run()