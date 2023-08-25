import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    API_KEY = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        # self.title = title
        # self.description = description
        # self.url = url
        # self.subs_count = subs_count
        # self.video_count = video_count
        # self.views_count = views_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.channel_id = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(self.channel_id, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    # def get_info(self):
    #     self.channel_id = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
    #     formatted_data = json.loads(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
    #     return formatted_data

    def to_json(self, file):
        with open(file, 'a', encoding='utf-8') as json_file:
            pass

    @property
    def title(self):
        # youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.channel_id = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
        return formatted_data['items'][0]['snippet']['title']

    @property
    def description(self):
        self.channel_id = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
        return formatted_data['items'][0]['snippet']['description']

    @property
    def url(self):
        self.channel_id = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
        return formatted_data['items'][0]['snippet']['thumbnails']['url']

    @property
    def subs_count(self):
        self.channel_id = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
        return formatted_data['items'][0]['statistics']['subscriberCount']

    @property
    def video_count(self):
        self.channel_id = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
        return formatted_data['items']['statistics']['videoCount']

    @property
    def views_count(self):
        self.channel_id = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(self.channel_id, indent=2, ensure_ascii=False))
        return formatted_data['items'][0]['statistics']['viewCount']
