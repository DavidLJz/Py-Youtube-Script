from pyyoutube import Api
from decouple import config
from json import dumps as json_dumps
import functions
from time import sleep

acctoken_path = config("ACCESS_TOKEN_PATH")

my_client_id = config("CLIENT_ID")
my_client_secret = config("CLIENT_SECRET")

token_data = functions.get_stored_access_token(acctoken_path)

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

  functions.store_access_token(token_model=token_model, acctoken_path=acctoken_path)
  
else:
  api = Api(access_token=token_data["access_token"])
  
while True:
  print("\nWaiting for input...")
  command = input().strip()

  if command.lower() == "playlists":
    playlists = functions.get_my_playlists(api)

    print( json_dumps(playlists, indent=2, default=str) )

  elif "playlist_videos" in command.lower():
    stringlist = command.split(" ", 1)

    if len(stringlist) == 1:
      print("Must provide playlist id")
    else:
      id = stringlist[1]
      videos = functions.get_videos_by_playlist_id(api, id)
      print( json_dumps(videos, indent=2, default=str) )
  
  elif "playlist " in command.lower():
    stringlist = command.split(" ", 1)

    if len(stringlist) == 1:
      print("Must provide playlist id")
    else:
      id = stringlist[1]
      playlist = functions.get_playlist_by_id(api, id)
      print( json_dumps(playlist, indent=2, default=str) )

  elif command == "exit" or command == "quit":
    quit(0)

  else:
    print("Command not valid")

  sleep(1)