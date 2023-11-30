import datetime
import os

import isodate
from googleapiclient.discovery import build


class APIMixin:
    """Класс-миксин для предоставления доступа к API."""
    api_key: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API youtube"""
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service


class PlayList(APIMixin):
    """Класс для работы с плей-листами ютуба"""

    def __init__(self, playlist_id):
        """Инициализируем id плейлиста по результатам запроса по API"""
        self.playlist_id = playlist_id
        self._init_from_api()

    def _init_from_api(self):
        """Получаем данные по API и инициализируем ими экземпляр класса"""
        playlist_info = self.get_service().playlists().list(id=self.playlist_id,
                                                            part='snippet,contentDetails').execute()
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails').execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

    def get_playlist_videos(self):
        """Возвращает ответ API на запрос всех видео плей-листа"""
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)).execute()
        return video_response

    @property
    def total_duration(self):
        """Возвращает суммарную длительность плей-листа в формате 'datetime.timedelta' (hh:mm:ss))"""
        video_response = self.get_playlist_videos()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self):
        """Выводит ссылку на самое залайканое видео в плейлисте"""
        video_response = self.get_playlist_videos()
        max_likes_count = 0
        max_likes_video_id = ''
        for item in video_response['items']:
            video_id = item['id']
            like_count = int(item['statistics']['likeCount'])
            if like_count > max_likes_count:
                max_likes_count = like_count
                max_likes_video_id = video_id
        return f'https://youtu.be/{max_likes_video_id}'
