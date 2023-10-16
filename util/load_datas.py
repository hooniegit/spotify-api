import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(current_dir, f'../lib')
data_dir = os.path.join(current_dir, f'../data')
sys.path.append(lib_dir)

from spotify import *
from database import *


# api request: browse/new_releases
def browse_new_releases(cnt):
    from time import time, sleep
    from datetime import datetime

    insert_date = datetime.now().strftime("%Y-%m-%d")
    endpoint = 'browse/new-releases'

    conn = open_connector()

    for page in range(0, 20):
        start_time = time()

        params = {
            'limit': '50',
            'offset': page * 50,
        }
        response = get_response(cnt=cnt, endpoint=endpoint, params=params)

        for item in response["albums"]["items"]:
            album_id = item["id"]
            release_date = item["release_date"]
            query_albums = f'''
                           INSERT IGNORE INTO albums (album_id, release_date, insert_date)
                           values (%s, %s, %s)
                           '''
            values = (album_id, release_date, insert_date)
            execute_query(conn, query_albums, values)

            for artist in item["artists"]: 
                artist_id = artist["id"]
                query_artists = f'''
                                INSERT IGNORE INTO artists (artist_id, insert_date)
                                VALUES (%s, %s)
                                '''
                values = (artist_id, insert_date)
                execute_query(conn, query_artists, values)
                query_relations = f'''
                                INSERT IGNORE INTO relations (album_id, artist_id)
                                VALUES (%s, %s)
                                '''
                values = (album_id, artist_id)
                execute_query(conn, query_relations, values)

        end_time = time()
        remain_time = 0.5 - (end_time - start_time)
        sleep(remain_time) if remain_time > 0 else sleep(0)

    conn.close()


# api request: browse/featured_playlists
def browse_featured_playlists(cnt):
    from time import time, sleep
    from datetime import datetime

    start_time = time()

    insert_date = datetime.now().strftime("%Y-%m-%d")
    insert_time = datetime.now().strftime("%H:%M:%S")
    endpoint = 'browse/featured-playlists'
    params = {    
        'country' : 'KR',
        'locale' : 'en_KR',
        'timestamp' : f'{insert_date}T{insert_time}',
        'limit' : 1,
        'offset' : 0
    }
    response = get_response(cnt=cnt, endpoint=endpoint, params=params)

    end_time = time()
    remain_time = 1 - (end_time - start_time)
    sleep(remain_time)      

    start_time = time()

    playlist_id = response['playlists']['items'].pop()['id']
    endpoint = f'playlists/{playlist_id}/tracks'
    params = {
        'market' : 'KR',
        'fields' : 'items(track(album(id,release_date),artists(id)))',
        'limit' : 50,
        'offset' : 0
    }
    response = get_response(cnt=cnt, endpoint=endpoint, params=params)
    
    conn = open_connector()

    for item in response['items'] :
        album_id = item['track']['album']['id']
        release_date = item['track']['album']['release_date']
        query_albums = f'''
                        INSERT IGNORE INTO albums (album_id, release_date, insert_date)
                        values (%s, %s, %s)
                        '''
        values = (album_id, release_date, insert_date)
        execute_query(conn, query_albums, values)

        for artist in item['track']['artists'] : 
            artist_id = artist['id']
            query_artists = f'''
                                INSERT IGNORE INTO artists (artist_id, insert_date)
                                VALUES (%s, %s)
                                '''
            values = (artist_id, insert_date)
            execute_query(conn, query_artists, values)

            query_artists = f'''
                                INSERT IGNORE INTO relations (album_id, artist_id)
                                VALUES (%s, %s)
                                '''
            values = (album_id, artist_id)
            execute_query(conn, query_artists, values)

    conn.close()

    end_time = time()
    remain_time = 0.5 - (end_time - start_time)
    sleep(remain_time) if remain_time > 0 else sleep(0)



# api request: artists/related_artists
def artists_related_artists(cnt, insert_date):
    from time import time, sleep

    conn = open_connector()

    query_search = f"""
                   SELECT artist_id FROM artists
                   WHERE insert_date = '{insert_date}'
                   """
    result = fetchall_query(conn=conn, query=query_search)
    id_list = [artist[0] for artist in result]

    for artist_id in id_list:
        start_time = time()

        endpoint = f'artists/{artist_id}/related-artists'
        response = get_response(cnt=cnt, endpoint=endpoint)
        for related_artist in response['artists']:
            related_artist_id = related_artist['id']
            query_artists = f'''
                            INSERT IGNORE INTO artists (artist_id, insert_date)
                            VALUES (%s, %s)
                            '''
            values = (related_artist_id, insert_date)
            execute_query(conn, query_artists, values)

        end_time = time()
        remain_time = 0.5 - (end_time - start_time)
        sleep(remain_time) if remain_time > 0 else sleep(0)

    conn.close()


# api request: artists/albums
# def artists_albums(cnt, insert_date):
#     from time import time, sleep

#     conn = open_connector()
#     query_search = f"""
#                    SELECT artist_id FROM artists
#                    WHERE insert_date = '{insert_date}'
#                    """
#     result = fetchall_query(conn=conn, query=query_search)
#     id_list = [artist[0] for artist in result]

#     for artist_id in id_list:
#         endpoint = f'artists/{artist_id}/albums'

#         start_time = time()
#         response = get_response(cnt=cnt, endpoint=endpoint)

#         for album in response['items']:
#             album_id = album['id']
#             release_date = album['release_date']
#             query_albums = f'''
#                             INSERT IGNORE INTO albums (album_id, release_date, insert_date)
#                             VALUES (%s, %s, %s)
#                             '''
#             values = (album_id, release_date, insert_date)
#             execute_query(conn, query_albums, values)

#             query_relations = f'''
#                             INSERT IGNORE INTO relations (album_id, artist_id)
#                             VALUES (%s, %s)
#                             '''
#             values = (album_id, artist_id)
#             execute_query(conn, query_relations, values)

#         end_time = time()
#         remain_time = 0.5 - (end_time - start_time)
#         sleep(remain_time) if remain_time > 0 else sleep(0)       

#     conn.close()


# api request: albums
def albums(cnt, insert_date):
    from time import time, sleep
    from files import file_json

    conn = open_connector()

    try: os.makedirs(f"{data_dir}/albums/{insert_date}")
    except: pass
    try: os.makedirs(f"{data_dir}/tracks/{insert_date}")
    except: pass

    query_search = f"""
                   SELECT album_id FROM albums
                   WHERE insert_date = '{insert_date}'
                   """
    result = fetchall_query(conn=conn, query=query_search)
    id_list = [album[0] for album in result]

    conn.close()

    for album_id in id_list:
        start_time = time()

        endpoint=f'albums/{album_id}'
        params={'market' : 'KR'}
        response = get_response(cnt=cnt, endpoint=endpoint, params=params)

        file_dir = f"{data_dir}/albums/{insert_date}/{album_id}.json"
        file_json(file_dir=file_dir, json_data=response)

        for track in response['tracks']['items']:
             track_id = track["id"]
             file_dir = f"{data_dir}/tracks/{insert_date}/{track_id}.json"
             file_json(file_dir=file_dir, json_data=track)

        end_time = time()
        remain_time = 0.5 - (end_time - start_time)
        sleep(remain_time) if remain_time > 0 else sleep(0)


# api request: artists
def artists(cnt, insert_date):
    from time import time, sleep
    from files import file_json

    conn = open_connector()

    try: os.makedirs(f"{data_dir}/artists/{insert_date}")
    except: pass

    query_search = f"""
                   SELECT artist_id FROM artists
                   WHERE insert_date = '{insert_date}'
                   """
    result = fetchall_query(conn=conn, query=query_search)

    conn.close()

    id_list = [artist[0] for artist in result]
    for id in id_list:
        start_time = time()

        endpoint = f'artists/{id}'
        params = {'market' : 'KR'}
        response = get_response(cnt=cnt, endpoint=endpoint, params=params)
        file_dir = f"{data_dir}/artists/{insert_date}/{id}.json"
        file_json(file_dir=file_dir, json_data=response)

        end_time = time()
        remain_time = 0.5 - (end_time - start_time)
        sleep(remain_time) if remain_time > 0 else sleep(0)


# api request: artists/albums
# multi-thread
def thread_artists_albums(insert_date):
    from threading import Thread
    from time import time, sleep

    conn = open_connector()

    query_search = f"""
                   SELECT artist_id FROM artists
                   WHERE insert_date = '{insert_date}'
                   """
    result = fetchall_query(conn=conn, query=query_search)
    id_list = [artist[0] for artist in result]

    conn.close()

    def do_work(id_list, cnt, insert_date):
        conn = open_connector()

        for artist_id in id_list:
            start_time = time()

            endpoint = f'artists/{artist_id}/albums'
            response = get_response(cnt=cnt, endpoint=endpoint)

            for album in response['items']:
                album_id = album['id']
                release_date = album['release_date']
                query_albums = f'''
                                INSERT IGNORE INTO albums (album_id, release_date, insert_date)
                                VALUES (%s, %s, %s)
                                '''
                values = (album_id, release_date, insert_date)
                execute_query(conn, query_albums, values)

                query_relations = f'''
                                INSERT IGNORE INTO relations (album_id, artist_id)
                                VALUES (%s, %s)
                                '''
                values = (album_id, artist_id)
                execute_query(conn, query_relations, values)

        conn.close()

        end_time = time()
        remain_time = 0.5 - (end_time - start_time)
        sleep(remain_time) if remain_time > 0 else sleep(0)  

    index_cnt = len(id_list) // 4
    index_remain = len(id_list) % 4

    big_list = []
    for i in range(4):
        small_list = id_list[i*index_cnt : (i+1)*index_cnt]
        big_list.append(small_list)
    big_list[-1] += id_list[-index_remain:]

    threads = []
    for j in range(len(big_list)):
        thread = Thread(target=do_work, args=(big_list[j], j+1, insert_date))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


# test
if __name__ == "__main__":
    # confirmed - 23.10.16
    # browse_new_releases(1)

    # confirmed - 23.10.16
    # browse_featured_playlists(1)

    # confirmed - 23.10.16
    # artists_related_artists(1, insert_date)

    # confirmed - 23.10.16
    # artists_albums(1, insert_date)

    # confirmed - 23.10.16
    # albums(1, insert_date)

    # confirmed - 23.10.16
    # artists(1, "2023-10-16")

    # confirmed - 23.10.16
    # thread_artists_albums("2023-10-16")
    pass