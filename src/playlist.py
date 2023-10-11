import datetime
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_info = youtube.playlists().list(id=playlist_id, part='snippet').execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        url = playlist_info['items'][0]['id']
        self.url = f'https://www.youtube.com/playlist?list={url}'

    def total_duration(self):
        pass

    def show_best_video(self):
        pass
