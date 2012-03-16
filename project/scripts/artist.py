'''
Script that traverses the applications table and populates the artist and 
application_artist tables.
'''
from project.settings import DATABASES
import MySQLdb

def get_or_create(cursor, artist_name):
    cursor.execute ("SELECT id FROM app_artist WHERE name=%s", artist_name)
    row = cursor.fetchone()
    if row:
        #artist already exists
        return row[0]
    
    cursor.execute("INSERT INTO app_artist (name) VALUES (%s)", artist_name)
    return cursor.lastrowid 

def save_artists(cursor):
    cursor.execute ("SELECT application_id, artist_name FROM epf_application")
    for row in cursor.fetchall():
        application_id, artist_name = row
        artist_id = get_or_create(cursor, artist_name)
        
        cursor.execute("""INSERT INTO app_applicationartist 
                        (application_id, artist_id) VALUES (%s, %s)""",
                        (application_id, artist_id))


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