import datetime
import os

import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_info = youtube.playlistItems().list(playlistId=playlist_id,
                                                     part='contentDetails').execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        url = playlist_info['items'][0]['id']
        self.url = f'https://www.youtube.com/playlist?list={url}'
        self.video_ids = [video['contentDetails']['videoId'] for video in playlist_info['items']]

    @property
    def total_duration(self):
        video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            print(duration)

    def show_best_video(self):
        video_response = youtube.videos().list(id=self.video_ids,
                                               part='snippet,statistics,contentDetails,topicDetails').execute()
        print(video_response)
        max_likes_count = 0
        for video in video_response['items']:
            print(video)
            if int(video['statistics']['likeCount']) > int(max_likes_count):
                max_likes_count = video['statistics']['likeCount']
                print(video['id'])
                video_id = video['id']
                return f'https://youtu.be/{video_id}'
