import main
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Output info of YT playlists')

  parser.add_argument("-id", help="ID of a playlist. If not given, shows all Your Playlists", default=None)
  parser.add_argument("-f", "--format", choices=["json","csv"], help="Output Format, defaults to JSON", default="json")

  args = parser.parse_args()

  main.run("pls_export", args)