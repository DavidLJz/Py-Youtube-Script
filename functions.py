from pyyoutube import Api, AccessToken
from json import dumps as json_dumps, load as json_load
from datetime import datetime, timedelta
from dateutil import parser as dt_parser
import os
import sys
import psutil
import traceback

def get_stored_access_token(acctoken_path:str):
  if os.path.isfile(acctoken_path) is False:
    return None

  with open(acctoken_path, "r") as f:
    token_data = json_load(f)
    f.close()

  if "access_token" not in token_data.keys():
    return None

  dt = dt_parser.parse(token_data["time"])
  dt_expire_time = dt + timedelta(seconds=token_data["expires_in"])

  print("dt_expire_time", dt_expire_time)

  if datetime.now() >= dt_expire_time:
    return None

  return token_data

def get_my_playlists(api:Api) -> list:
  data = api.get_playlists(mine=True, count=None)
  return format_playlists_data_items(data.items)

def get_playlist_by_id(api:Api, id:str) -> list:
  data = api.get_playlist_by_id(playlist_id=id)
  return format_playlists_data_items(data.items)

def format_playlists_data_items(items:list) -> list:
  playlists = []

  for item in items:
    playlist_data = {
      "publishedAt": item.snippet.publishedAt,
      "title": item.snippet.title,
      "description": item.snippet.description,
      "thumbnails": item.snippet.thumbnails.high.url,
      "privacyStatus": item.status.privacyStatus,
      "videos": item.contentDetails.itemCount
    }

    playlists.append(playlist_data)

  return playlists

def get_videos_by_playlist_id(api:Api, id:str):
  data = api.get_playlist_items(playlist_id=id)
  return format_video_data_items(data.items)

def format_video_data_items(items:list) -> list:
  videos = []

  for item in items:
    video_data = {
      "id": item.contentDetails.videoId,
      "publishedAt": item.snippet.publishedAt,
      "title": item.snippet.title,
      "description": item.snippet.description,
      "thumbnails": item.snippet.thumbnails.high.url,
      "privacyStatus": item.status.privacyStatus
    }

    videos.append(video_data)

  return videos

def store_access_token(token_model:AccessToken, acctoken_path:str):
  token_data = {
    "access_token": token_model.access_token,
    "expires_in": token_model.expires_in,
    "time": datetime.now()
  }

  with open(acctoken_path, "w") as f:
    f.write(json_dumps(token_data, default=str))
    f.close()

def restart_program():
  """Restarts the current program, with file objects and descriptors
      cleanup
  """

  try:
    p = psutil.Process(os.getpid())

    if hasattr(p, 'get_open_files'):
      for handler in p.get_open_files() + p.connections():
        os.close(handler.fd)

  except:
    print(traceback.format_exc())

  python = sys.executable
  os.execl(python, python, *sys.argv)