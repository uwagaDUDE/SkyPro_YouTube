from dotenv import dotenv_values
from googleapiclient.discovery import build
import json
import os

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
        channel_data = open(f'{channel_id}.json', 'w', encoding="UTF-8")
        channel_data.write(f'{self.data}')
        channel_data.close()
        self.data = open(f'{channel_id}.json', 'r', encoding="UTF-8")
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
    # print(channel1.information_output()) # Общая информация о канале
    # channel_info.to_json('channel_data.json') # Сохранение в файл
    # Во время обработки запроса создается файл с данными канала, его лучше удалить
    os.remove(f'{"UCwEthvsKuX9ZaqvIaGfG3RQ"}.json')
    os.remove(f'{"UCPx7nkXKVp7iOnxANvMm4HQ"}.json')