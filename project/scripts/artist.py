'''
Script that traverses the applications table and populates the artist and 
application_artist tables.
'''
from project.settings import DATABASES
import MySQLdb


def save_artists(cursor):
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


def run():
    conn = MySQLdb.connect (host = DATABASES['default']['HOST'],
                            user = DATABASES['default']['USER'],
                            passwd = DATABASES['default']['PASSWORD'],
                            db = DATABASES['default']['NAME'])
    cursor = conn.cursor ()

    save_artists(cursor)
        
    cursor.close()
    conn.close()

run()