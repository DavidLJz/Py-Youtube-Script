# To Do
Write a proper README.MD

# Usage

## 1. Create Google Cloud Credentials for a Desktop Application
[Read More Here](https://developers.google.com/identity/protocols/oauth2#installed)

## 2. Set environment variables
First, customize the `.env.example` file with your own parameters, and then rename it to `.env`.

```
# Path to save the access token file
ACCESS_TOKEN_PATH=C:\pyyt\access_token.json

# Path to download JSON and CSV data
OUTPUT_PATH=C:\pyyt\output

# Google Oauth2 Client Id
CLIENT_ID=myclientid

# Google Oauth2 Client Secret
CLIENT_SECRET=myclientsecret
```

## 3. First run
Execute any of the scripts on command line, on first run you will be asked to authorize the Python Scripts to access your Google account data.

```
>> python .\playlists.py
Please kindly open the following URL for authorization :D
 https://accounts.google.com/o/oauth2/v2/auth...
^^^ That one!

Once thats done click on allow and you will be redirected to a URL on "localhost"
Copy the whole url and paste it into this window
```

Just follow the instructions and an `access_token.json` file will be saved to the `ACCESS_TOKEN_PATH`.

From now on you can run any of the commands avaiblable:
- playlists.py
- videos.py
- playlists_export.py
- videos_export.py