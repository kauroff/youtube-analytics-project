import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    __API_KEY = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self._init_from_api()

    def _init_from_api(self) -> None:
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{channel["items"][0]["id"]}'
        self.subs_count = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(channel['items'][0]['statistics']['videoCount'])
        self.views_count = int(channel['items'][0]['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey=self.__API_KEY)
        channel_id = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel_id, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API youtube."""
        return build('youtube', 'v3', developerKey=cls.__API_KEY)

    def get_info(self) -> None:
        channel_id = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        formatted_data = json.loads(json.dumps(channel_id, indent=2, ensure_ascii=False))
        return formatted_data

    def to_json(self, file) -> None:
        """Сохраняет данные экземпляра класса в файл."""
        dict_to_write = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subs_count,
            'video_count': self.video_count,
            'view_count': self.views_count,
        }
        with open(file, 'w', encoding='utf-8') as filename:
            json.dump(dict_to_write, filename)

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subs_count + other.subs_count

    def __sub__(self, other):
        return self.subs_count - other.subs_count

    def __gt__(self, other):
        if self.subs_count > other.subs_count:
            return True
        return False

    def __ge__(self, other):
        if self.subs_count >= other.subs_count:
            return True
        return False

    def __lt__(self, other):
        if self.subs_count < other.subs_count:
            return True
        return False

    def __le__(self, other):
        if self.subs_count <= other.subs_count:
            return True
        return False
