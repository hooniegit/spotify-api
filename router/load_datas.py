from fastapi import APIRouter
from util.load_datas import *

router = APIRouter()

# [1]
@router.get("/mysql/new_release")
async def get_browse_new_releases(cnt:int):
	return browse_new_releases(cnt)

# [2]
@router.get("/mysql/featured_playlists")
async def get_browse_featured_playlists(cnt:int):
	return browse_featured_playlists(cnt)

# [3]
@router.get("/mysql/related_artists")
async def get_artists_related_artists(insert_date:str):
	return thread_artists_related_artists(insert_date)

# [4]
@router.get("/mysql/artist_albums")
async def get_artists_albums(insert_date:str):
	return thread_artists_albums(insert_date)

# [5]
@router.get("/json/albums")
async def get_albums(insert_date:str):
	return thread_albums(insert_date)

# [6]
@router.get("/json/artists")
async def get_artists(insert_date:str):
	return thread_artists(insert_date)
