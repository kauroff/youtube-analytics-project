import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    API_KEY = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        channel_id = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel_id, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def get_info(self):
        channel_id = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(channel_id, indent=2, ensure_ascii=False))
        return formatted_data

    def to_json(self, file):
        with open(file, 'a', encoding='utf-8') as json_file:
            json_file.write(json.dumps(self.get_info()))

    @property
    def title(self):
        return self.get_info()['items'][0]['snippet']['title']

    @property
    def description(self):
        return self.get_info()['items'][0]['snippet']['description']

    @property
    def url(self):
        url = f'https://www.youtube.com/channel/{self.__channel_id}'
        return url

    @property
    def subs_count(self):
        return self.get_info()['items'][0]['statistics']['subscriberCount']

    @property
    def video_count(self):
        return self.get_info()['items'][0]['statistics']['videoCount']

    @property
    def views_count(self):
        return self.get_info()['items'][0]['statistics']['viewCount']
