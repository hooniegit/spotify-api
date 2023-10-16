from fastapi import APIRouter
from util.load_hdfs import *

router = APIRouter()

# [7]
@router.get("/hdfs/albums")
async def to_hdfs_albums(insert_date:str):
	return albums_to_hdfs(insert_date)

# [8]
@router.get("/hdfs/artists")
async def to_hdfs_artists(insert_date:str):
	return artists_to_hdfs(insert_date)

# [9]
@router.get("/hdfs/tracks")
async def to_hdfs_tracks(insert_date:str):
	return tracks_to_hdfs(insert_date)