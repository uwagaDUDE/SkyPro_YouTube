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

    def __init__(self, channel, channel_id):
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
        self.data = open(f'channel_data.json', 'r', encoding="UTF-8")
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

        except Exception:
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


if __name__ == '__main__':

    while search != False:

        channel_id = input('Введите ID канала: ')
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        channel_info = UserInformation(channel, channel_id)

        try:
            print(channel_info.information_output())
            #os.remove(f'{channel_id}.json') для автоматического удаления данных о канале, если потребуется

        except Exception as Error:
            print(f'Ошибка поиска YouTube-канала, проверьте правильность введеного ID.'
                  f'{Error}')
