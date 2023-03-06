from dotenv import dotenv_values
from googleapiclient.discovery import build
import json
import os
import requests

#Проверяем введен ли api_key в .env, и существует ли он вообще,
#если нет то создаем и просим ввести ключ

try:
    api_key = dotenv_values('.env')['YOUTUBE_API']

except Exception as Error:
    dotenv_file = open('.env', 'w', encoding='UTF-8')
    new_api = input('API ключ не найден, введите API ключ: ')
    dotenv_file.write(f'YOUTUBE_API={new_api}')
    dotenv_file.close()
    api_key = dotenv_values('.env')['YOUTUBE_API']

youtube = build('youtube', 'v3', developerKey=api_key)
search = True


class UserInformation:

    def __init__(self, channel='', channel_id=''):
        """
        Получение данных о канале, записывая их в файл
        :param channel_id: Нужен для создания файла с названием ID канала
        :param self.channel_name: Название канала
        :param self.channel_description: Описание канала
        :param self.channel_view_count: Общее количество просмотров на канале
        :param self.channel_subs: Количество подписчиков на канале
        :param self.channel_videos: Количество видео на канале
        :param channel:
        """
        self.data = json.dumps(channel, indent=2, ensure_ascii=False)
        if self.ethernet_connection() == 200:
            channel_data = open(f'./cache/channels/{channel_id}.json', 'w', encoding="UTF-8")
            channel_data.write(f'{self.data}')
            channel_data.close()
            self.data = open(f'./cache/channels/{channel_id}.json', 'r', encoding="UTF-8")
        else:
            try:
                self.data = open(f'./cache/channels/{channel_id}.json', 'r', encoding="UTF-8")
            except Exception:
                print('Не удалось получить информацию о канале.')

        """
        Получаем информацию канала
        """
        try:
            self._channel_id = channel_id
            self.channel_url = f'https://www.youtube.com/channel/{channel_id}'
            self.channel_data_loads = json.load(self.data)
            self.channel_data = self.channel_data_loads['items'][0]
            self.channel_name = self.channel_data['snippet']['title']
            self.channel_description = self.channel_data['snippet']['description']
            self.channel_statistics = self.channel_data['statistics']
            self.channel_view_count = self.channel_statistics['viewCount']
            self.channel_subs = self.channel_statistics['subscriberCount']
            self.channel_videos = self.channel_statistics['videoCount']
            self.data.close()

        except Exception as Error:
            pass

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, id):
        if self.channel_id_checker(id):
            raise AttributeError('property "channel_id" of "Channel" object has no setter')
        self._channel_id = id

    def channel_id_checker(self, new_id):
        return self.channel_id != new_id

    def get_service(self):
        return youtube

    def information_output(self):
        """
        Функция вывода информации
        Разделил ее отступами, чтобы информация не сливалась
        :return:
        """
        return f'\nНазвание канала: {self.channel_name}\n'\
            f'\nОписание канала: {self.channel_description}\n'\
            f'\nЧисло подписчиков: {self.channel_subs}\n'\
            f'Общее число просмотров: {self.channel_view_count}\n'\
            f'Количество видео-роликов на канале: {self.channel_videos}\n' \
            f'Ссылка на канал - {self.channel_url}'

    def to_json(self, file_name=''):
        """Сохраняет данные экземпляра класса в файл."""
        dict_to_write = {'Channel name':self.channel_name,
                         'Channel ID':self.channel_id,
                         'Channel description':self.channel_description,
                         'Channel subscribers':self.channel_subs,
                         'Channel views':self.channel_view_count,
                         'Channel videos':self.channel_videos,
                         'Channel url':self.channel_url}
        with open(file_name, 'w', encoding='UTF-8') as fp:
            json.dump(dict_to_write, fp)
        fp.close()

    def search_function(self):
        """
        Циклический поиск
        :return: Информация о канале и возможность сохарнить ее
        """

        while search != False:

            channel_id = input('Введите ID канала: ')
            channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
            channel_info = UserInformation(channel, channel_id)

            try:
                print(channel_info.information_output())
                file_save = input('Сохранить файл с данными о канале?\n'
                                  '(y/n): ')
                if file_save == 'y':
                    channel_info.to_json('channel_data.json')
                    print('Данные сохранены в файл channel_data.json')
                    os.remove(f'{channel_id}.json') #УДАЛИТЕ ЭТУ СТРОКУ, ЕСЛИ ТРЕБУЕТСЯ СОХРАНЯТЬ КАЖДЫЕ ДАННЫЕ
                else:
                    os.remove(f'{channel_id}.json') #УДАЛИТЕ ЭТУ СТРОКУ, ЕСЛИ ТРЕБУЕТСЯ СОХРАНЯТЬ КАЖДЫЕ ДАННЫЕ
                    pass

            except Exception as Error:
                print(f'Ошибка поиска YouTube-канала, проверьте правильность введеного ID.\n'
                      f'{Error}')

    def ethernet_connection(self):
        #Просто захотелось)
        yt_response = requests.get('https://www.youtube.com/')
        return yt_response.status_code

    def __int__(self):
        return int(self.channel_subs)

    def __str__(self):
        return f'YouTube-Канал: {self.channel_name}'

    def __gt__(self, other):
        if int(self.channel_subs) > int(other):
            return True
        else:
            return False

    def __add__(self, other):
        return int(self.channel_subs)+int(other)

class Video:

    def __init__(self, video_id='', video_name=''): # ,9lO06Zxhu88, BBotskuyw_M
        """
        Реализовал так же через создание файла, мне с этим удобнее работать
        Чтобы не засорять корневую папку, перенес создаваемые файлы в папку cache.
        :param video_id: Айди нужного нам видео
        """
        self.video_id = video_id
        self.video_name = video_name
        # self.video_likes = video_likes
        # self.video_views = video_views
        video = youtube.videos().list(id=video_id, part='snippet,statistics').execute()
        if self.ethernet_connection() == 200:
            self.video_loads = json.dumps(video, indent=2, ensure_ascii=False)
            with open(f'./cache/videos/video_{video_id}.json', 'w', encoding='UTF-8') as video_file:
                video_file.write(self.video_loads)
                video_file.close()
                try:
                    self.video_name = self.video_data()['items'][0]['snippet']['title']
                    self.video_views = self.video_data()['items'][0]['statistics']['viewCount']
                    self.video_likes = self.video_data()['items'][0]['statistics']['likeCount']
                except Exception as error:
                    print(f'{error}')

        else:
            try:
                self.video_name = self.video_data()['items'][0]['snippet']['title']
                self.video_views = self.video_data()['items'][0]['statistics']['viewCount']
                self.video_likes = self.video_data()['items'][0]['statistics']['likeCount']
            except Exception:
                raise Exception(f'Не возможно получить информацию о видео')

    def video_data(self):
        with open(f'./cache/videos/video_{self.video_id}.json', 'r', encoding='UTF-8') as video_file:
            return json.load(video_file)

    def cache_video_data(self):
        with open(f'./cache/videos/video_{self.video_id}.json', 'r', encoding='UTF-8') as video_file:
            self.video_data = json.load(video_file)
            try:
                self.video_name = self.video_data['items'][0]['snippet']['title']
                self.video_views = self.video_data['items'][0]['statistics']['viewCount']
                self.video_likes = self.video_data['items'][0]['statistics']['likeCount']
                return f'\nНазвание видео-ролика: "{self.video_name}"\n' \
                       f'Количество просмотров: {self.video_views}\n' \
                       f'Количество лайков: {self.video_likes}\n'
            except Exception as error:
                return f'{error}'
    def ethernet_connection(self):
        yt_response = requests.get('https://www.youtube.com/')
        return yt_response.status_code

    def __str__(self):
        return f'Название видео: {self.video_name}'
class PLVideo(Video):

    def __init__(self, video_id, playlist_id=''):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        playlist = youtube.playlists().list(part='snippet', id=playlist_id).execute()
        pl_data = json.dumps(playlist, indent=2, ensure_ascii=False)
        with open(f'./cache/playlists/pl_{playlist_id}.json', 'w', encoding='UTF-8') as playlist_file:
            playlist_file.write(pl_data)
            playlist_file.close()
        with open(f'./cache/playlists/pl_{playlist_id}.json', 'r', encoding='UTF-8') as playlist_file:
            try:
                self.pl_data = json.load(playlist_file)
                self.pl_name = self.pl_data['items'][0]['snippet']['title']

            except Exception:
                print('Ошибка')

    def __str__(self):
        return f'Название видео: {self.video_name} \n' \
               f'Плейлист: {self.pl_name}'


def clear_cache():
    """
    Функция очистки папки с кэшем
    :return:
    """
    cache_dir = './cache'
    for root, dirs, files in os.walk(cache_dir):
        for file in files:
            os.remove(os.path.join(root, file))

if __name__ == '__main__':

    # UserInformation().search_function() # Запуск циклического поиска.

    """
    Вызов информации о канале отдельно
    """
    channel = youtube.channels().list(id='UCwEthvsKuX9ZaqvIaGfG3RQ', part='snippet,statistics').execute()
    channel1 = UserInformation(channel, 'UCwEthvsKuX9ZaqvIaGfG3RQ')
    channel = youtube.channels().list(id='UCPx7nkXKVp7iOnxANvMm4HQ', part='snippet,statistics').execute()
    channel2 = UserInformation(channel, 'UCPx7nkXKVp7iOnxANvMm4HQ')
    print(channel1) # Название канала
    print(channel2)
    print(channel1 > channel2)
    print(channel1 + channel2)
    print(PLVideo('9lO06Zxhu88', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD'))
    # clear_cache()