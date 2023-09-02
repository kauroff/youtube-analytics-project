import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    """Класс для видео с Ютуб"""

    def __init__(self, id_video):
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=id_video).execute()
        self.id_video = id_video
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.id_video}'
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist

    def __str__(self):
        return f'{self.video_title}'
