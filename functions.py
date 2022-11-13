from pyyoutube import Api, AccessToken
from json import dumps as json_dumps, load as json_load
from datetime import datetime, timedelta
from dateutil import parser as dt_parser
import os
from csv import writer as csv_writer, QUOTE_MINIMAL

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
  data = api.get_playlist_items(playlist_id=id, count=None)
  return format_video_data_items(data.items)

def format_video_data_items(items:list) -> list:
  videos = []

  for item in items:
    try:
      thumbnail = item.snippet.thumbnails.high.default
    except:
      thumbnail = ""

    video_data = {
      "id": item.contentDetails.videoId,
      "publishedAt": item.snippet.publishedAt,
      "title": item.snippet.title,
      "description": item.snippet.description,
      "thumbnails": thumbnail,
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

  save_json(acctoken_path, token_data)

def save_json(path:str, data):
  with open(path, "w") as f:
    f.write( json_dumps(data, default=str) )
    f.close()

def save_csv(path:str, data:list) -> bool:
  if len(data) == 0:
    return False
    
  with open(path, "w", newline="", encoding="utf-8") as f:
    csvw = csv_writer(f, delimiter=",", quotechar='"', quoting=QUOTE_MINIMAL)
    
    for i in range(len(data)):
      item = data[i]

      if i == 0:
        header = item.keys()
        csvw.writerow(header)

      item = item.values()

      csvw.writerow(item)

    f.close()

  return True

def get_api(acctoken_path:str, my_client_id:str, my_client_secret:str):
  '''
  Returns the Authenticated API object
  '''

  token_data = get_stored_access_token(acctoken_path)

  if token_data is None:
    api = Api(client_id=my_client_id, client_secret=my_client_secret)

    auth_url = api.get_authorization_url()

    print(
      "Please kindly open the following URL for authorization :D\n", auth_url[0], "\n^^^ That one!\n"
    )

    print("Once thats done click on allow and you will be redirected to a URL on \"localhost\"")

    print("Copy the whole url and paste it into this window")

    url = input().strip()

    token_model = api.generate_access_token(authorization_response=url)

    store_access_token(token_model=token_model, acctoken_path=acctoken_path)
    
  else:
    api = Api(access_token=token_data["access_token"])

  return api