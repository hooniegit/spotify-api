import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, f'../../lib')
sys.path.append(lib_dir)

from database import *

# drop spotify tables
# use only for test
def drop_tables():
    conn = open_connector()

    query = f'''
    DROP TABLE IF EXISTS relations
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    query = f'''
    DROP TABLE IF EXISTS albums
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    query = f'''
    DROP TABLE IF EXISTS artists
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    conn.close()


# create albums table
def create_table_albums():
    conn = open_connector()
    query = f'''
    CREATE TABLE IF NOT EXISTS albums(
        id INT AUTO_INCREMENT,
        album_id VARCHAR(30) PRIMARY KEY,
        release_date VARCHAR(10),
        insert_date DATE,
        UNIQUE KEY unique_column (id)
    )
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    conn.close()


# create artists table
def create_table_artists():
    conn = open_connector()
    query = f'''
    CREATE TABLE IF NOT EXISTS artists(
        id INT AUTO_INCREMENT,
        artist_id VARCHAR(30) PRIMARY KEY,
        insert_date DATE,
        UNIQUE KEY unique_column (id)
    )
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    conn.close()


# create relations table
def create_table_relations():
    conn = open_connector()
    query = f'''
    CREATE TABLE IF NOT EXISTS relations(
        album_id VARCHAR(30),
        artist_id VARCHAR(30),
        FOREIGN KEY (album_id) REFERENCES albums(album_id),
        FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
        UNIQUE KEY unique_combination (album_id, artist_id)
    )
    '''
    cursor = conn.cursor()
    cursor.execute(query)

    conn.close()


if __name__ == "__main__":
    # confirmed - 23.10.16
    drop_tables()
    create_table_albums()
    create_table_artists()
    create_table_relations()