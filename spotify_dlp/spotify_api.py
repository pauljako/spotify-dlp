import json, requests, re, urllib.parse


class spotify_api:
   def __init__(self, client_id, client_secret):
      headers = {"Content-Type": "application/x-www-form-urlencoded"}
      data = f"grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

      result = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

      content = json.loads(result.content)
      if ("error" in content): raise Exception(content["error"])

      self.token = json.loads(result.content)["access_token"]


   def get_request(self, uri):
      headers = {"Authorization": "Bearer " + self.token}
      result = requests.get("https://api.spotify.com/v1" + uri, headers=headers)

      content = json.loads(result.content)
      if ("error" in content): raise Exception(content["error"]["message"])

      return content


   def get_tracks_info(self, url):
      def get_item_info(item, album_name=None):
         print(item["album"])
         info = {
            "id": item["id"],
            "name": item["name"],
            "authors": [artist["name"] for artist in item["artists"]],
            "album": album_name if album_name else item["album"]["name"],
            "album_image": item["album"]["images"][0],
            "album_release": item["album"]["release_date"],
            "album_raw": item["album"],
            "explicit": item["explicit"],
            "url": item["external_urls"]["spotify"]
         }

         query = f"{info['name']} {' '.join(info['authors'])} {info['album']}"
         info["query"] = urllib.parse.quote_plus(query)

         return info

      def flatten(input_list):
         result = []
         for item in input_list:
            if isinstance(item, list): result.extend(flatten(item))
            else: result.append(item)
         return result

      type, id = self.clean_url(url)

      match(type):
         case "album":
            album_name = self.get_request(f"/albums/{id}")["name"]
            result = self.get_request(f"/albums/{id}/tracks")
            info = [get_item_info(item, album_name) for item in result["items"]]

         case "artist":
            result = self.get_request(f"/artists/{id}/top-tracks?market=US")
            info = [get_item_info(item) for item in result["tracks"]]

         case "playlist":
            result = self.get_request(f"/playlists/{id}/tracks")
            info = [get_item_info(item["track"]) for item in result["items"]]

         case "track":
            result = self.get_request(f"/tracks?ids={id}")
            info = [get_item_info(item) for item in result["tracks"]]

      return info

   def get_search_info(self, query, search_type="track", search_count=1):
      result = self.get_request(f"/search?q={query}&type={search_type}&limit={search_count}")
      result = list(result.values())[0]["items"]

      if (len(result) == 0): raise Exception("No tracks were found!")

      info = self.get_tracks_info(f"https://open.spotify.com/{search_type}/{result[0]['id']}")

      return info


   @staticmethod
   def clean_url(url, begstr="spotify.com/", endstr="?"):
      beg = url.find(begstr)
      if (beg == -1): beg = 0
      else: beg += len(begstr)

      end = url.find(endstr, beg)
      if (end == -1): end = len(url)

      return url[ beg : end ].split("/")




############### TESTING ###############
#
#import os
#spotify = spotify_api(os.getenv("SPOTIFY_DLP_CLIENT_ID"), os.getenv("SPOTIFY_DLP_CLIENT_SECRET"))
#
#
#"""
#https://open.spotify.com/album/09wqWIOKWuS6RwjBrXe08B?si=3266fb2161824070
#https://open.spotify.com/artist/7jy3rLJdDQY21OgRLCZ9sD?si=4a55232349a94d48
#https://open.spotify.com/playlist/7mBgbujFe7cAZ5rrK0HTxp?si=82b3e3f2549641b5
#https://open.spotify.com/track/6rDaCGqcQB1urhpCrrD599?si=05987dc8f4ae4d31
#https://open.spotify.com/album/32bR4LcEc1PvJEhaKoo4ZN?si=bNNN-JInSwep0o4J04pojw
#"""
#
#
#query = "meteora"
#search_type = "album"
#
#print(json.dumps(
#   spotify.get_tracks_info("https://open.spotify.com/album/32bR4LcEc1PvJEhaKoo4ZN?si=bNNN-JInSwep0o4J04pojw"),
#   indent=3
#))
