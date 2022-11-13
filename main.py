from decouple import config
from json import dumps as json_dumps
from datetime import datetime
from os import path, makedirs
import functions

def get_default_output_path(ext:str) -> str:
  makedirs(config("OUTPUT_PATH"), exist_ok=True)

  now = datetime.now().strftime("%Y-%m-%d_%H%M")
  path = config("OUTPUT_PATH") + f"\{now}"

  return path + ext

def run(command:str, args):
  acctoken_path = config("ACCESS_TOKEN_PATH")
  my_client_id = config("CLIENT_ID")
  my_client_secret = config("CLIENT_SECRET")

  api = functions.get_api(acctoken_path, my_client_id, my_client_secret)
    
  if command == "playlists":
    if args.id is None:
      result = functions.get_my_playlists(api)

    else:
      result = functions.get_playlist_by_id(api, args.id)

  elif command == "pls_export":
    if args.id is None:
      result = functions.get_my_playlists(api)

    else:
      result = functions.get_playlist_by_id(api, args.id)

    if args.format == "json":
      args.output = get_default_output_path(".json")
    elif args.format == "csv":
      args.output = get_default_output_path(".csv")

  elif command == "videos":
    if args.playlist_id is None:
      result = {}

    else:
      result = functions.get_videos_by_playlist_id(api, args.playlist_id)

  elif command == "vid_export":
    if args.playlist_id is None:
      result = {}

    else:
      result = functions.get_videos_by_playlist_id(api, args.playlist_id)

    if args.format == "json":
      args.output = get_default_output_path(".json")
    elif args.format == "csv":
      args.output = get_default_output_path(".csv")

  if args.output is None:
    print( json_dumps(result, indent=2, default=str) )
  
  else:
    if args.format == "json":
      functions.save_json(args.output, result)
      saved = True

    elif args.format == "csv":
      saved = functions.save_csv(args.output, result)

    if saved is True:
      print("Saved to " + args.output)
    else:
      print("error saving output")