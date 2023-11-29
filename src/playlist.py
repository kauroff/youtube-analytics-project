import datetime
import os

import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_info = youtube.playlists().list(id=self.playlist_id, part='snippet,contentDetails').execute()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        url = playlist_info['items'][0]['id']
        # self.url = playlist_info['thumbnails']['default']['url']
        self.url = f'https://www.youtube.com/playlist?list={url}'
        self.video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

    @property
    def total_duration(self):
        video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        video_response = youtube.videos().list(id=self.video_ids,
                                               part='snippet,statistics,contentDetails,topicDetails').execute()
        max_likes_count = 0
        for item in video_response['items']:
            video_id = item['id']
            like_count = int(item['statistics']['likeCount'])
            if like_count > max_likes_count:
                max_likes_count = like_count
                max_likes_video_id = video_id
        return f'https://youtu.be/{max_likes_video_id}'
