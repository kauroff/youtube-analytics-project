import datetime
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

    def function(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        return playlist_videos


pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
print(pl.function())
