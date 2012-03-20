'''
Creates a table with the top100
'''
#from project.settings import DATABASES
from settings import DATABASES
import MySQLdb
from datetime import datetime, timedelta
import time

TABLE_NAME = 'app_updatedapps'

def save_updated(cursor):
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

    save_updated(cursor)
        
    cursor.close()
    conn.close()

run()