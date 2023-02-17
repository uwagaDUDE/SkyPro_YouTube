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

    def __init__(self, channel):
        self.data = json.dumps(channel, indent=2, ensure_ascii=False)
        channel_data = open('channel_data.json', 'w', encoding="UTF-8")
        channel_data.write(f'{self.data}')
        channel_data.close()
        self.data = open('channel_data.json', 'r', encoding="UTF-8")
        """
        Получаем информацию канала
        """
        try:

            self.channel_data_loads = json.load(self.data)
            self.channel_data =self.channel_data_loads['items'][0]
            self.channel_name = self.channel_data['snippet']['title']
            self.channel_description = self.channel_data['snippet']['description']
            self.channel_statistics = self.channel_data['statistics']
            self.channel_view_count = self.channel_statistics['viewCount']
            self.channel_subs = self.channel_statistics['subscriberCount']
            self.channel_videos = self.channel_statistics['videoCount']

        except Exception:
            pass

    def information_output(self):
        '''
        Функция вывода информации
        :return:
        '''
        return print(f'\nНазвание канала: {self.channel_name}\n'
                     f'\nОписание канала: {self.channel_description}\n'
                     f'\nЧисло подписчиков: {self.channel_subs}\n'
                     f'Общее число просмотров: {self.channel_view_count}\n'
                     f'Количество видео-роликов на канале: {self.channel_videos}\n')


while search != False:

    channel_id = input('Введите ID канала: ')
    channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
    #print(json.dumps(channel, indent=2, ensure_ascii=False))
    try:
        UserInformation(channel).information_output()
        os.remove('channel_data.json')
    except Exception:
        print(f'Ошибка поиска YouTube-канала, проверьте правильность введеного ID.')