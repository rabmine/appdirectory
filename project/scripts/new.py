'''
Creates a table with the top100
'''
#from project.settings import DATABASES
from settings import DATABASES
import MySQLdb
from datetime import datetime

TABLE_NAME = 'app_newapps'

def save_new(cursor):
    cursor.execute("TRUNCATE TABLE {table}".format(table=TABLE_NAME))
    
    cursor.execute("""INSERT INTO {table} (application_id) SELECT application_id
                    FROM epf_application WHERE itunes_release_date > %s"""
                    .format(table=TABLE_NAME), datetime.now())

def run():
    conn = MySQLdb.connect (host = DATABASES['default']['HOST'],
                            user = DATABASES['default']['USER'],
                            passwd = DATABASES['default']['PASSWORD'],
                            db = DATABASES['default']['NAME'])
    cursor = conn.cursor ()

    save_new(cursor)
        
    cursor.close()
    conn.close()

run()