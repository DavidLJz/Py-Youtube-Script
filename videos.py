import main
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Output info of YT videos')

  parser.add_argument("-id", help="ID of a video", default=None)
  parser.add_argument("-p", "--playlist_id", help="ID of a playlist", default=None)

  parser.add_argument("-o", "--output", help="Ouput path", default=None)
  parser.add_argument("-f", "--format", choices=["json","csv"], help="Output Format, defaults to JSON", default="json")

  args = parser.parse_args()

  main.run("videos", args)